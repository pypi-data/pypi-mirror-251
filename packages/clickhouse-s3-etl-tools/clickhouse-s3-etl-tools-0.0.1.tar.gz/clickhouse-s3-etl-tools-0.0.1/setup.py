from setuptools import setup, find_packages


def load_requirements(file_name):
    requirements = []
    with open(file_name, "r") as file:
        for line in file:
            # Remove comments and strip whitespace
            line = line.split("#")[0].strip()
            if line:
                requirements.append(line)
    return requirements


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clickhouse-s3-etl-tools",
    version="0.0.1",
    packages=find_packages(),
    author='Dmitry Utiralov',
    author_email='d.utiralov@netology.tech',
    description='',
    long_description=long_description,
    install_requires=load_requirements("requirements.txt"),
    extras_require={
        "dev": load_requirements("dev-requirements.txt"),
    },
    include_package_data=True,
    # python_requires='>=3.10',
    # entry_points={
    #     "console_scripts": [
    #         "s3_exporter = clickhouse_s3_etl_tools.s3_exporter.__main__:run_service",
    #         "s3_to_clickhouse_transfer = clickhouse_s3_etl_tools.s3_to_clickhouse_transfer.__main__:run_service",
    #     ]
    # },
)
