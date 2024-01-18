import os
import json
import uuid
import ast
from string import Template
from enum import Enum
from itertools import chain
import pandas as pd
import pkg_resources
from urllib.parse import urlparse
import duckdb
import altair as alt
import psutil
import vegafusion as vf
from abc import ABC, abstractmethod
from IPython.display import display, HTML
from IPython.core.magic import (register_line_magic, register_cell_magic)

vf.enable(row_limit=None, mimetype="vega")


class ChartType(Enum):
    BAR = 'bar'
    LINE = 'line'
    SCATTER = 'scatter'


class ColumnType(Enum):
    ORDINAL = ':O'
    NOMINAL = ':N'
    QUANTITATIVE = ':Q'
    TEMPORAL = ':T'


class AbstractChart(ABC):
    def __init__(self, data, x_column, y_column, x_aggregate=None, y_aggregate=None, x_type=None, y_type=None, width=720, height=350):
        self.data = data
        self.x_column = x_column
        self.y_column = y_column
        self.x_aggregate = x_aggregate
        self.y_aggregate = y_aggregate
        self.x_type = x_type
        self.y_type = y_type
        self.width = width
        self.height = height

    def _get_encoding(self, axis):
        aggregate = getattr(self, axis + '_aggregate', None)
        column = getattr(self, axis + '_column', None)
        column_type = getattr(self, axis + '_type', None)
        encoding_str = f'{aggregate}({column})' if aggregate else column
        return [encoding_str, encoding_str + f'{column_type}' if column_type else encoding_str]

    def _get_encoded_chart(self, chart):
        [x_label, x_encoding] = self._get_encoding('x')
        [y_label, y_encoding] = self._get_encoding('y')
        encoded_chart = chart.encode(
            x=alt.X(
                x_encoding,
                title=x_label,
                axis=alt.Axis(labelOverlap=True)
            ),
            y=alt.Y(
                y_encoding,
                title=y_label,
                axis=alt.Axis(labelOverlap=True)
            ),
            tooltip=[x_label, y_label],
        ).properties(width=self.width, height=self.height)
        return encoded_chart

    @abstractmethod
    def create_chart(self):
        pass


class BarChart(AbstractChart):
    def create_chart(self):
        encoded_chart = self._get_encoded_chart(
            alt.Chart(self.data).mark_bar())
        return encoded_chart


class LineChart(AbstractChart):
    def create_chart(self):
        encoded_chart = self._get_encoded_chart(
            alt.Chart(self.data).mark_line())
        return encoded_chart


class ScatterChart(AbstractChart):
    def create_chart(self):
        encoded_chart = self._get_encoded_chart(
            alt.Chart(self.data).mark_circle())
        return encoded_chart


def create_dynamic_chart(chart_type_str, data, x_column, y_column, x_aggregate=None, y_aggregate=None, x_type=None, y_type=None, width=720, height=350):
    chart_type = ChartType(chart_type_str)
    if chart_type == ChartType.BAR:
        chart = BarChart(data, x_column, y_column, x_aggregate,
                         y_aggregate, x_type, y_type, width, height).create_chart()
    elif chart_type == ChartType.LINE:
        chart = LineChart(data, x_column, y_column, x_aggregate,
                          y_aggregate, x_type, y_type, width, height).create_chart()
    elif chart_type == ChartType.SCATTER:
        chart = ScatterChart(data, x_column, y_column, x_aggregate,
                             y_aggregate, x_type, y_type, width, height).create_chart()
    else:
        raise ValueError(
            "Invalid chart type. Supported types: 'bar', 'line', 'scatter'")
    file_path = str(uuid.uuid4())+'.json'
    # display(chart)
    vf.save_vega(chart, file_path)
    f = open(file_path, "r")
    file_content = f.read()
    os.remove(file_path)
    return file_content


class BucketUrl(object):

    def __init__(self, url):
        self._parsed = urlparse(url, allow_fragments=False)

    @property
    def bucket(self):
        return self._parsed.path.lstrip('/').split("/")[0]

    @property
    def file_name(self):
        return self._parsed.path.lstrip('/').split("/")[1]

    @property
    def url(self):
        return self._parsed.geturl()

    @property
    def gcs_url(self):
        return f"gcs:/{self._parsed.path}"


class BucketData:
    def __init__(
            self, file_url, storage_options=None
    ):
        self.storage_options = storage_options or {"token": "cloud"}
        self.bucket_url_obj = BucketUrl(file_url)
        self._file_type = self._detect_file_type()

    def _detect_file_type(self):
        file_extension = self.bucket_url_obj.file_name.split(".")[-1]
        if file_extension == "csv":
            return "csv"
        elif file_extension == "json":
            return "json"
        elif file_extension == "parquet":
            return "parquet"
        elif file_extension == "xlsx" or file_extension == "xls":
            return "excel"
        else:
            raise Exception("File type not supported")

    def _load_csv_data(self):
        return pd.read_csv(self.bucket_url_obj.gcs_url, storage_options=self.storage_options)

    def _load_json_data(self):
        return pd.read_json(self.bucket_url_obj.gcs_url, storage_options=self.storage_options)

    def load_data(self) -> pd.DataFrame:
        if self._file_type == "csv":
            data = self._load_csv_data()
        elif self._file_type == "json":
            data = self._load_json_data()
        else:
            raise Exception("Unsupported file type")

        return data


class AbstractKernelUtils:
    @staticmethod
    def list_packages():
        pass

    @staticmethod
    def add_secret():
        pass

    @staticmethod
    def makeResponse(self, temporary_response):
        try:
            return temporary_response.to_json(orient="records")
        except Exception as e:
            return temporary_response

    @staticmethod
    def fetch_resource_usage():
        cpu_info = {
            "CPU Cores": psutil.cpu_count(logical=False),
            "Logical CPUs": psutil.cpu_count(logical=True),
            "CPU Usage (%)": psutil.cpu_percent(interval=1),
        }

        mem_info = {
            "Total Memory (GB)": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "Available Memory (GB)": round(psutil.virtual_memory().available / (1024 ** 3), 2),
            "Used Memory (GB)": round(psutil.virtual_memory().used / (1024 ** 3), 2),
            "Memory Usage (%)": psutil.virtual_memory().percent,
        }

        resource_usage_details = {"CPU": cpu_info, "Memory": mem_info}
        # resource_usage_details = json.dumps(resource_usage_details)
        return resource_usage_details


class KernelUtils(AbstractKernelUtils):
    @staticmethod
    def list_packages():
        installed_packages = pkg_resources.working_set
        res = list(
            map(lambda x: {"name": x.key, "version": x.version}, installed_packages))
        return json.dumps(res)

    @staticmethod
    def add_secret(secrets_list: list, secret_object: dict):
        code_string: str = ""
        for secret in secrets_list:
            code_string += "\\n"
            code_string += f'{secret["secret_name"]}="{secret["secret_value"]}"'
        parsed = ast.parse(code_string)
        code = compile(parsed, filename='', mode='exec')
        exec(code, secret_object)
        print("Secret Added Successfully")
        return True


class Source:

    connection = None

    def connect(self, *args):
        pass

    def close(self):
        pass

    def execute_query(self, query):
        pass

    def get_tables(self):
        pass

    def get_table_schema(self, table_name):
        pass


class Posgtres(Source):
    connection = None
    get_tables_query: str = "SELECT table_name, table_schema FROM information_schema.tables WHERE  table_type = 'BASE TABLE' AND table_schema NOT LIKE 'pg_%' AND table_schema != 'information_schema';"
    get_table_schema_query = Template(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '$schema' AND table_name = '$table_name';")

    def connect(self, host, port, database, user, password):
        from sqlalchemy import create_engine
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e

    def get_tables(self):
        return self.execute_query(self.get_tables_query)

    def get_table_schema(self, table_name):
        [schema, table_name] = table_name.split(".")
        return self.execute_query(self.get_table_schema_query.substitute(schema=schema, table_name=table_name))


class MySql(Source):
    connection = None
    get_tables_query: str = "SELECT table_name FROM information_schema.tables WHERE  table_type = 'BASE TABLE' AND table_schema NOT LIKE 'pg_%' AND table_schema != 'information_schema';"
    get_table_schema_query = Template(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '$schema' AND table_name = '$table_name';")

    def connect(self, host, port, database, user, password):
        from sqlalchemy import create_engine
        db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e

    def get_tables(self):
        return self.execute_query(self.get_tables_query)

    def get_table_schema(self, table_name):
        [schema, table_name] = table_name.split(".")
        return self.execute_query(self.get_table_schema_query.substitute(schema=schema, table_name=table_name))


class RedShift(Source):
    connection = None
    get_tables_query: str = "SELECT table_name FROM information_schema.tables WHERE  table_type = 'BASE TABLE' AND table_schema NOT LIKE 'pg_%' AND table_schema != 'information_schema';"
    get_table_schema_query = Template(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '$schema' AND table_name = '$table_name';")

    def connect(self, host, port, database, user, password):
        from sqlalchemy import create_engine
        db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e

    def get_tables(self):
        return self.execute_query(self.get_tables_query)

    def get_table_schema(self, table_name):
        [schema, table_name] = table_name.split(".")
        return self.execute_query(self.get_table_schema_query.substitute(schema=schema, table_name=table_name))


class ClickHouse(Source):
    connection = None

    def connect(self, host, port, database, user, password):
        from sqlalchemy import create_engine
        db_url = f"f'clickhouse://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e


class BigQuery(Source):
    connection = None
    get_tables_query = Template(
        "SELECT table_name FROM $dataset.INFORMATION_SCHEMA.TABLES;")
    get_table_schema_query = Template(
        "SELECT column_name, data_type FROM `$dataset.INFORMATION_SCHEMA.COLUMNS` WHERE table_name = '$table_name';")

    def connect(self, project_id, private_key_id, private_key, client_email, client_id):
        from google.cloud import bigquery

        service_account_info = json.dumps({
            "type": "service_account",
            "project_id": project_id,
            "private_key_id": private_key_id,
            "private_key": private_key,
            "client_email": client_email,
            "client_id": client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_client_email@your_project.iam.gserviceaccount.com"
        })

        self.connection = bigquery.Client.from_service_account_info(
            json.loads(service_account_info))

    def execute_query(self, query):
        try:
            query = query.strip()
            query_job = self.connection.query(query)
            return query_job.result().to_dataframe()
        except Exception as e:
            return e

    def get_tables(self):
        datasets = self.connection.list_datasets()
        tables: list = []
        for dataset in datasets:
            query: str = self.get_tables_query.substitute(
                dataset=dataset.dataset_id)
            get_tables_query_response = list(
                map(lambda x: {"dataset_name": dataset.dataset_id, "table_name": x["table_name"]}, self.connection.query(query).result()))
            tables.append(get_tables_query_response)
        return pd.DataFrame(list(chain(*tables)))

    def get_table_schema(self, table_name):
        [dataset, table_name] = table_name.split(".")
        return self.execute_query(self.get_table_schema_query.substitute(dataset=dataset, table_name=table_name))


class MemoryDf(Source):
    connection = None

    def execute_query(self, query):
        return duckdb.query(query).to_df()


class SnowFlake(Source):

    connection = None
    connection = None
    get_tables_query: str = "SELECT table_name, table_schema FROM information_schema.tables WHERE table_type = 'BASE TABLE';"
    get_table_schema_query = Template(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '$schema' AND table_name = '$table_name';")

    def connect(self, username, password, account, database, warehouse):
        from sqlalchemy import create_engine
        db_url = f"snowflake://{username}:{password}@{account}/{database}?warehouse={warehouse}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e

    def get_tables(self):
        return self.execute_query(self.get_tables_query)

    def get_table_schema(self, table_name):
        [schema, table_name] = table_name.split(".")
        return self.execute_query(self.get_table_schema_query.substitute(schema=schema, table_name=table_name))


class DataBricks(Source):

    connection = None
    get_tables_query: str = "SHOW TABLES"
    get_table_schema_query = Template("DESCRIBE EXTENDED $table_name")

    def connect(self, token, host, port, database, http_path):
        from sqlalchemy import create_engine
        db_url = f"databricks://token:{token}@{host}:{port}/{database}?http_path={http_path}"
        engine = create_engine(db_url)
        self.connection = engine.connect()
        print("Connection Successful")
        return True

    def close(self):
        self.connection.close()
        return True

    def execute_query(self, query):
        from sqlalchemy import text
        query = text(query.strip())
        transaction = self.connection.begin()
        try:
            result = self.connection.execute(query)
            transaction.commit()
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        except Exception as e:
            transaction.rollback()
            return e

    def get_tables(self):
        return self.execute_query(self.get_tables_query)

    def get_table_schema(self, table_name):
        return self.execute_query(self.get_table_schema_query.substitute(table_name=table_name))


class Bucket(Source):
    connection = duckdb.connect(database=':memory:')

    def connect(self, file_url, integration_name):
        df = BucketData(file_url).load_data()
        self.connection.register(f'{integration_name}', df)
        return True

    def close(self):
        pass

    def execute_query(self, query):
        try:
            return self.connection.execute(query).fetchdf()
        except Exception as e:
            return e


class ConnectionManager:
    connections: dict = {}
    mapper: dict = {
        "POSTGRES": Posgtres,
        "MYSQL": MySql,
        "REDSHIFT": RedShift,
        "BIGQUERY": BigQuery,
        "SNOWFLAKE": SnowFlake,
        "DATABRICKS": DataBricks,
        "CLICKHOUSE": ClickHouse,
        "BUCKET": Bucket
    }

    def __init__(self):
        self.connections["DUCKDB"] = MemoryDf()

    def makeResponse(self, temporary_response):
        try:
            return temporary_response.to_json(orient="records")
        except Exception as e:
            return temporary_response

    def connectSource(self, id, type, *args):
        if self.connections.get(id):
            pass
        self.connections[id] = self.mapper[type]()
        self.connections[id].connect(*args)

    def executeQueryOnSource(self, query: str, id):
        return self.connections[id].execute_query(query=query)

    def getTablesFromSource(self, id):
        connection: Source = self.connections[id]
        return self.makeResponse(connection.get_tables())

    def getTableSchemaFromSource(self, id, table_name):
        connection: Source = self.connections[id]
        return self.makeResponse(connection.get_table_schema(table_name=table_name))


connectionManager = ConnectionManager()
secrets = {}
print("INITIALIZED")
