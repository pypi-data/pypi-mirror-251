import logging
import snowflake.snowpark as snowpark

from abc import ABC
from pyspark.sql import DataFrame
from wells_data_pipeline_cores.commons import EnvVariables
from wells_data_pipeline_cores.services.spark import SparkDataService
from wells_data_pipeline_cores.services.snow import SnowDataService


class CurationService(ABC):
    """
    CurationSerice is base (abstract) class. It provides common/utility mehtods to do curation pipelines
    """

    def __init__(self, env_vars: EnvVariables) -> None:
        self.env_vars: EnvVariables = env_vars

    @staticmethod
    def _get_snowpark_service(
        env_vars: EnvVariables,
        schema_conf_name: str = "default",
    ) -> SnowDataService:
        return SnowDataService(
            env_vars=env_vars,
            schema_conf_name=schema_conf_name,
        )

    @staticmethod
    def _get_spark_service(
        env_vars: EnvVariables, snow_conf: str = "default"
    ) -> SparkDataService:
        return SparkDataService(env_vars=env_vars, snow_conf=snow_conf)

    # Methods related to SnowDataService
    def get_target_table(
        self, service: SnowDataService, table_name: str
    ) -> snowpark.Table:
        return service.get_target_table(table_name=table_name)

    def query_snow_data(
        self, service: SnowDataService, query: str
    ) -> snowpark.DataFrame:
        return service.query_data(query=query)

    def upsert_snow_data(
        self,
        tbl_target: snowpark.Table,
        dd_source: snowpark.DataFrame,
        primary_key_name: str,
    ) -> snowpark.MergeResult:
        return SnowDataService._upsert_data(
            tbl_target=tbl_target,
            dd_source=dd_source,
            primary_key_name=primary_key_name,
        )

    def write_dataframe_to_snow(
        self, df: snowpark.DataFrame, table_name: str, save_mode: str = "errorifexists"
    ):
        df.write.mode(save_mode).save_as_table(table_name=table_name)

    # Methods related to SparkDataService
    def get_target_table(self, service: SparkDataService, table_name: str) -> DataFrame:
        return service.get_target_table(table_name=table_name)

    def query_snow_data(self, service: SparkDataService, query: str) -> DataFrame:
        return service.query_snow(query=query)

    def upsert_snow_data(
        self,
        service: SparkDataService,
        df: DataFrame,
        table_name: str,
        primary_key: str = "ID",
    ):
        service.upsert_snow_data(
            df=df,
            table_name=table_name,
            primary_key=primary_key,
        )

    def write_dataframe_to_snow(
        self,
        service: SparkDataService,
        df: DataFrame,
        table_name: str,
        save_mode: str = "errorifexists",
    ):
        service.write_dataframe_to_snow(df, table_name, save_mode)
