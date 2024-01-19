import logging
import uuid
from abc import ABC
from wells_data_pipeline_cores.commons import EnvVariables
from pyspark.sql import SparkSession, DataFrame
from pyspark import SparkContext
from snowflake.connector.pandas_tools import write_pandas


class SparkDataService(ABC):
    def __init__(self, env_vars: EnvVariables, snow_conf: str):
        self.env_vars: EnvVariables = env_vars
        self.session: SparkSession = env_vars.pyspark
        self.snow_conf: str = snow_conf
        self.snow_conn_params = SparkDataService._get_snow_conn_params(
            self.snow_conf, self.env_vars
        )

    def query_snow(self, query: str) -> DataFrame:
        """
        Queries snowflake based on the snowflake configuration name passed in

        Parameters
        ----------
        query: Query statement to execute

        Returns
        -------
        DataFrame containing query results
        """
        return (
            self.session.read.format("snowflake")
            .options(**self.snow_conn_params)
            .option("query", query)
            .load()
        )

    def get_target_table(self, table_name: str) -> DataFrame:
        return (
            self.session.read.format("snowflake")
            .options(**self.snow_conn_params)
            .option("dbtable", table_name)
            .load()
        )

    def upsert_snow_data(
        self,
        df: DataFrame,
        table_name: str,
        primary_key: str = "ID",
    ):
        """
        Creates a Snowflake MERGE command to upsert the dataframe to the specified table

        Parameters
        ----------
        session : SparkSession to use for upsert
        snow_conf: Name of Snowflake config defined in conf/ folder
        df: Source DataFrame containing the rows that need to be upserted
        table_name: Destination Snowflake table name
        primary_key: Primery key used for joining source and destination data

        Returns
        -------
        DataFrame containing upsert results
        """
        target_tbl = self.get_target_table(table_name)

        missing_cols = list(set(target_tbl.columns) - set(df.columns))
        if len(missing_cols) > 0:
            logging.error(
                "upsert_snow_data(....) - missing columns in dataframe source: ",
                missing_cols,
            )
        else:
            # Write DataFrame to a staging table
            staging_table_name = f"STG_{table_name}_{uuid.uuid4().hex.upper()}"
            logging.info(
                f"upsert_snow_data() - creating staging table: {staging_table_name}"
            )
            self.write_dataframe_to_snow(df, staging_table_name, "overwrite")

            # Build Snowflake Merge query
            updates = []
            insert_values = []
            for col in target_tbl.columns:
                insert_values.append(f"s.{col}")
                if col != primary_key:
                    updates.append(f"{col} = s.{col}")

            update_clause = ", ".join(updates)
            insert_fields_clause = ", ".join(target_tbl.columns)
            insert_values_clause = ", ".join(insert_values)

            merge_query = """
                MERGE INTO {target_tbl} t USING {staging_tbl} s
                ON t.{primary_key} = s.{primary_key}
                WHEN MATCHED THEN UPDATE SET {updates}
                WHEN NOT MATCHED THEN INSERT ({fields}) VALUES ({inserts})
            """.format(
                target_tbl=table_name,
                staging_tbl=staging_table_name,
                primary_key=primary_key,
                updates=update_clause,
                fields=insert_fields_clause,
                inserts=insert_values_clause,
            )

            # Run Merge query and delete staging table
            sfUtils = self.session.sparkContext._jvm.net.snowflake.spark.snowflake.Utils
            logging.info("upsert_snow_data() - running merge query on snowflake")
            sfUtils.runQuery(self.snow_conn_params, merge_query)

            logging.info("upsert_snow_data() - dropping staging table from snowflake")
            sfUtils.runQuery(self.snow_conn_params, f"drop table {staging_table_name}")

    def write_dataframe_to_snow(
        self,
        df: DataFrame,
        table_name: str,
        save_mode: str = "errorifexists",
    ):
        """
        Writes the DataFrame to the specified table in Snowflake.
        Args:
            snow_conf: Name of Snowflake config defined in conf/ folder
            df: Snowpark DataFrame to write
            table_name: Table name in snowpark where the data is written to
            save_mode: One of the following strings.
                "append": Append data of this DataFrame to existing data.
                "overwrite": Overwrite existing data.
                "errorifexists": Throw an exception if data already exists.
                "ignore": Ignore this operation if data already exists.
                Default value is "errorifexists".
        """
        df.write.format("snowflake").options(**self.snow_conn_params).option(
            "dbtable", table_name
        ).mode(save_mode).save()

    def update_snow_connection(
        self,
        database: str = None,
        schema: str = None,
        role: str = None,
        warehouse: str = None,
    ):
        if database is not None:
            self.snow_conf["sfDatabase"] = database

        if schema is not None:
            self.snow_conf["sfScheme"] = schema

        if role is not None:
            self.snow_conf["sfRole"] = role

        if warehouse is not None:
            self.snow_conf["sfWarehouse"] = warehouse

        self.snow_conn_params = SparkDataService._get_snow_conn_params(
            self.snow_conf, self.env_vars
        )

    @staticmethod
    def _get_snow_conn_params(snow_conf: str, env_vars: EnvVariables):
        """
        Returns snowflake connections parameters in the format required by Spark Connector
        """
        snow_parameters = env_vars.kepler_conf.get_snowpark_conn_params(snow_conf)
        host = env_vars.kepler_conf.get_snow_host()

        return {
            "sfUrl": host,
            "sfUser": snow_parameters["user"],
            "sfPassword": snow_parameters["password"],
            "sfRole": snow_parameters["role"],
            "sfDatabase": snow_parameters["database"],
            "sfSchema": snow_parameters["schema"],
            "sfWarehouse": snow_parameters["warehouse"],
        }
