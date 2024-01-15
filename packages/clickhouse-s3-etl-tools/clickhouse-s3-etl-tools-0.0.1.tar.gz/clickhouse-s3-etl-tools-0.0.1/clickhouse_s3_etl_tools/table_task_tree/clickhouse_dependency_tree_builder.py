from typing import Dict, Tuple, List, Any
from urllib.parse import urlparse

from clickhouse_driver import Client

ADD_TOPMIND_TABLES: bool = False


class TableNode:
    """
    Represents a node in the table dependency graph.
    """

    def __init__(self, identifier: Tuple[str, str]):
        self.id = identifier

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return isinstance(other, TableNode) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class DependencyTableDict:
    """
    Represents a dictionary containing dependencies between tables.
    """

    def __init__(self):
        self.dependency_dict: Dict[TableNode, TableNode] = {}


def update_dependency_dict(
        dict_for_update: DependencyTableDict, main_dict: DependencyTableDict
) -> DependencyTableDict:
    """
    Updates the main dependency dictionary with the entries from another dictionary.

    Args:
        dict_for_update (DependencyTableDict): The dictionary to update from.
        main_dict (DependencyTableDict): The main dictionary to update.

    Returns:
        DependencyTableDict: The updated main dictionary.
    """
    main_dict_copy = {}
    dict_for_update_reverse = {
        value: key for key, value in dict_for_update.dependency_dict.items()
    }

    for node, parent in main_dict.dependency_dict.items():
        current_node = node

        if current_node in main_dict_copy:
            current_parent = main_dict_copy[current_node]
            if (
                    current_parent in dict_for_update_reverse
                    and dict_for_update_reverse[current_parent] != current_node
            ):
                main_dict_copy[current_node] = dict_for_update_reverse[current_parent]

        if (
                current_node in dict_for_update.dependency_dict
                and current_node not in main_dict_copy
        ):
            parent_trigger_node = dict_for_update.dependency_dict[current_node]

            for node_, parent_ in main_dict.dependency_dict.items():
                if node_.id == current_node.id:
                    main_dict_copy[current_node] = parent_trigger_node
                    main_dict_copy[parent_trigger_node] = parent_

            for node_, parent_ in main_dict.dependency_dict.items():
                if parent_.id == parent_trigger_node.id:
                    if node_ in dict_for_update.dependency_dict:
                        parent_trigger_node_ = dict_for_update.dependency_dict[node_]
                        main_dict_copy[node_] = parent_trigger_node_
                        main_dict_copy[parent_trigger_node_] = current_node
                    else:
                        main_dict_copy[node_] = current_node
                    main_dict_copy[current_node] = parent_

        elif current_node not in main_dict_copy:
            main_dict_copy[current_node] = parent

    main_dict.dependency_dict = main_dict_copy
    return main_dict


def get_dict_dependencies(
        url: str, databases: List[str]
) -> Tuple[DependencyTableDict, List[Dict[str, Any]]]:
    """
    Retrieve dependencies between tables from ClickHouse.

    Parameters:
    - url (str): The URL of the ClickHouse instance.
    - databases (List[str]): List of databases to consider.

    Returns:
    Tuple[DependencyTableDict, List[Dict[str, Any]]]: Tuple containing the dictionary representing dependencies
    between tables and a list of table configurations.
    """
    url = urlparse(url)
    conn_params = {
        "host": url.hostname,
        "port": url.port or 9000,
        "database": url.path.lstrip("/"),
        "user": url.username,
        "password": url.password,
    }

    client = Client(**conn_params)

    databases_str = ",".join([f"'{d}'" for d in databases])
    query = f"""SELECT  table, 
                        database, 
                        ifNull(total_rows,0) as total_rows,
                        dependencies_database, 
                        dependencies_table, 
                        engine,
                        arrayElement(extractAll(create_table_query, 'TO (\\S+)'), 1) AS extracted_table_name, 
                        arrayElement(extractAll(as_select, 'FROM (\\S+)'), -1) AS extracted_table_name_from
              FROM system.tables 
              WHERE database in ({databases_str}) """

    result = client.execute(query)

    parents_by_id = DependencyTableDict()
    trigger_with_parent = DependencyTableDict()
    tables = []

    for row in result:
        table_config = {
            "TABLE_NAME": row[0],
            "DATABASE": row[1],
            "TOTAL_ROWS": row[2],
            "DEPENDENCIES_DATABASE": row[3],
            "DEPENDENCIES_TABLE": row[4],
            "ENGINE": row[5],
            "EXTRACTED_TABLE_NAME": row[6],
            "EXTRACTED_TABLE_NAME_FROM": row[7],
        }

        tables.append(table_config)

        global_root = TableNode(("Global", "root"))
        table_node = TableNode((table_config["TABLE_NAME"], table_config["DATABASE"]))

        parents_by_id.dependency_dict.setdefault(table_node, global_root)

        for dep_db, dep_table in zip(
                table_config["DEPENDENCIES_DATABASE"], table_config["DEPENDENCIES_TABLE"]
        ):
            if dep_db not in databases and dep_db != "topmind":
                raise Exception(
                    f"The table {table_node} depends on {dep_db}.{dep_table}, but the specified database is not in the selected list of databases."
                )

            if dep_db != "topmind":
                table_node_dep = TableNode((dep_table, dep_db))
                parents_by_id.dependency_dict[table_node_dep] = table_node

        if (
                table_config["EXTRACTED_TABLE_NAME"] != ""
                and table_config["ENGINE"] == "MaterializedView"
        ):
            db_ext, table_ext = table_config["EXTRACTED_TABLE_NAME"].split(".")
            table_node_ext = TableNode((table_ext, db_ext))
            trigger_with_parent.dependency_dict[table_node] = table_node_ext

        if table_config["EXTRACTED_TABLE_NAME_FROM"] != "" and table_config[
            "ENGINE"
        ] in ("View", "MaterializedView"):
            db_view, table_view = table_config["EXTRACTED_TABLE_NAME_FROM"].split(".")
            if db_view not in databases and db_view != "topmind":
                raise Exception(
                    f"The table {table_node} depends on {db_view}.{table_view}, but the specified database is not in the selected list of databases."
                )

            if db_view != "topmind":
                table_node_view = TableNode((table_view, db_view))
                parents_by_id.dependency_dict[table_node] = table_node_view

    update_dependency_dict(trigger_with_parent, parents_by_id)
    assert len(tables) == len(set(parents_by_id.dependency_dict.keys()))
    return parents_by_id, tables
