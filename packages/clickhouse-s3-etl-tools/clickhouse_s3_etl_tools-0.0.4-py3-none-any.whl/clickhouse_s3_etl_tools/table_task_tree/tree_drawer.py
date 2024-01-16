from anytree import Node as AnyNode, RenderTree

from .clickhouse_dependency_tree_builder import TableNode


def generate_tree(parents_by_id):
    """
    Generate a tree structure from the dictionary of dependencies.

    Parameters:
    - parents_by_id: DependencyTableDict, the dictionary representing dependencies between tables.

    Returns:
    AnyNode: The root node of the generated tree.
    """
    root_id = "root.Global"
    global_node = AnyNode(root_id)
    nodes_by_id = {root_id: global_node}

    def set_parent(node_: TableNode, parent_: TableNode):
        node_id_str: str = f"{node_.id[1]}.{node_.id[0]}"
        parent_id_str: str = f"{parent_.id[1]}.{parent_.id[0]}"

        if node_id_str in nodes_by_id:
            return nodes_by_id[node_id_str]

        if parent_id_str in nodes_by_id and node_id_str not in nodes_by_id:
            nodes_by_id[node_id_str] = AnyNode(
                node_id_str, parent=nodes_by_id[parent_id_str]
            )
            return nodes_by_id[node_id_str]

        if parent_id_str not in nodes_by_id:
            try:
                nodes_by_id[node_id_str] = AnyNode(
                    node_id_str,
                    parent=set_parent(parent_, parents_by_id.dependency_dict[parent_]),
                )
            except KeyError as e:
                raise Exception(
                    f"The table {node_id_str} depends of the table {parent_id_str}. But this table doesn't exists"
                ) from e
            return nodes_by_id[node_id_str]
        return nodes_by_id[node_id_str]

    for node, parent in parents_by_id.dependency_dict.items():
        set_parent(node, parent)

    return global_node


def print_dependency_tree(root):
    """
    Print the dependency tree.

    Parameters:
    - root: AnyNode, the root node of the tree.
    """
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")
