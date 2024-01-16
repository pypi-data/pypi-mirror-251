import builtins

from pyspark.conf import SparkConf
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.avro.functions import *
from pyspark.sql.column import _to_java_column
from confluent_kafka.schema_registry import SchemaRegistryClient

from delta.tables import *

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    Pivot,
    MinuteRange,
    MetricType,
    MetricAggregation,
    BatchRunReportsRequest,
    RunRealtimeReportRequest,
    RunReportRequest,
    RunReportResponse,
    RunPivotReportRequest,
    GetMetadataRequest,
    Filter,
    FilterExpression,
    FilterExpressionList,
    OrderBy
)


#########
# SPARK #
#########
def get_spark_session(spark_conf: list, app_name: str, log_level: str) -> SparkSession:
    spark_conf = SparkConf().setAll(spark_conf)

    spark_session = SparkSession.builder.appName(app_name).config(conf=spark_conf).getOrCreate()

    spark_session.sparkContext.setLogLevel(log_level)

    return spark_session


def get_spark_conf(name: str, conf: list) -> dict:
    return dict(list(builtins.filter(lambda source: source['name'] == name, conf))[0])


#########
# KAFKA #
#########
def get_kafka_certificate_password() -> str:
    with open("/mnt/secrets/cluster-ca-cert/ca.password") as f:
        return f.read()


def get_kafka_user_password() -> str:
    with open("/mnt/secrets/my-user/user.password") as f:
        return f.read()


def read_kafka_stream(spark_session: SparkSession, spark_job_conf: dict, source_name: str) -> DataFrame:
    source_conf = get_spark_conf(source_name, spark_job_conf['sources'])
    raw_stream = spark_session \
        .readStream \
        .format("kafka") \
        .options(**source_conf['kafka_options']) \
        .load()

    deserialized_stream = deserialize_register_avro_stream(raw_stream, source_conf['kafka_deserialization'])

    return deserialized_stream


def read_kafka(spark_session: SparkSession, source_conf: dict) -> DataFrame:
    raw_stream = spark_session \
        .read \
        .format("kafka") \
        .options(**source_conf['kafka_options']) \
        .load()

    deserialized_stream = deserialize_register_avro_stream(raw_stream, source_conf['kafka_deserialization'])

    return deserialized_stream


def write_kafka_stream(stream: DataFrame, spark_job_conf: dict, output_name):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])

    stream = serialize_register_avro_stream(stream, output_stream_conf['kafka_serialization'])

    if output_stream_conf.get('processing_time') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("kafka") \
            .options(**output_stream_conf['kafka_options']) \
            .trigger(processingTime=output_stream_conf['processing_time']) \
            .outputMode(output_stream_conf['mode']) \
            .start()
    elif output_stream_conf.get('availableNow') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("kafka") \
            .options(**output_stream_conf['kafka_options']) \
            .trigger(availableNow=output_stream_conf['availableNow']) \
            .outputMode(output_stream_conf['mode']) \
            .start()
    elif output_stream_conf.get("once") is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .queryName(output_stream_conf['name']) \
            .format("kafka") \
            .options(**output_stream_conf['kafka_options']) \
            .trigger(once=output_stream_conf['once']) \
            .outputMode(output_stream_conf['mode']) \
            .start()
    else:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("kafka") \
            .options(**output_stream_conf['kafka_options']) \
            .outputMode(output_stream_conf['mode']) \
            .start()


def write_kafka(dataframe: DataFrame, spark_job_conf: dict, output_name: str):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])

    df = serialize_register_avro_stream(dataframe, output_stream_conf['kafka_serialization'])

    df.write.format("kafka").options(**output_stream_conf['kafka_options']).save()


######
# S3 #
######
def read_s3_compress_log_stream(spark_session: SparkSession, spark_job_conf: dict, source_name: str) -> DataFrame:
    source_stream_conf = get_spark_conf(source_name, spark_job_conf['sources'])
    return spark_session \
        .readStream \
        .options(**source_stream_conf['s3_options']) \
        .schema(source_stream_conf['schema']) \
        .text(source_stream_conf['location'])


##############
# DELTA LAKE #
##############
def create_delta_tables_if_not_exists(conf, schema):
    DeltaTable \
        .createIfNotExists() \
        .addColumns(schema) \
        .partitionedBy(conf["delta_options"]["partition_columns"]) \
        .location(conf["delta_options"]["location"]) \
        .property("delta.enableChangeDataFeed", conf["delta_options"]["enableChangeDataFeed"]) \
        .execute()


def create_delta_tables_if_not_exists_no_partitioning(conf, schema):
    DeltaTable \
        .createIfNotExists() \
        .addColumns(schema) \
        .location(conf["delta_options"]["location"]) \
        .execute()


def read_delta(spark_session: SparkSession, spark_job_conf: dict, source_name: str) -> DataFrame:
    source_conf = get_spark_conf(source_name, spark_job_conf['sources'])
    return spark_session \
        .read \
        .format("delta") \
        .options(**source_conf['delta_options']) \
        .load(source_conf["location"])


def read_delta_stream(spark_session: SparkSession, spark_job_conf: dict, source_name: str) -> DataFrame:
    source_stream_conf = get_spark_conf(source_name, spark_job_conf['sources'])
    return spark_session \
        .readStream \
        .format("delta") \
        .options(**source_stream_conf['delta_options']) \
        .load(source_stream_conf["location"])


def write_delta(spark_job_conf: dict, output_name: str, df: DataFrame):
    output_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists(output_conf, output_conf['delta_options']['schema'])
    (
        df
        .write
        .format("delta")
        .mode(output_conf['mode'])
        .partitionBy(output_conf['delta_options']['partition_columns'])
        .option("checkpointLocation", output_conf['checkpoint_location'])
        .option("partitionOverwriteMode", output_conf['delta_options']['partition_overwrite_mode'])
        .option("mergeSchema", output_conf['delta_options']['merge_schema'])
        .option("overwriteSchema", output_conf['delta_options']['overwrite_schema'])
        .save(output_conf['delta_options']['location'])
    )


def write_delta_no_partitioning(spark_job_conf: dict, output_name: str, df: DataFrame):
    output_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists(output_conf, output_conf['delta_options']['schema'])
    (
        df
        .write
        .format("delta")
        # Fixme: output_conf['delta_options']['mode'] -> output_conf['mode']
        .mode(output_conf['delta_options']['mode'])
        .option("checkpointLocation", output_conf['checkpoint_location'])
        .option("partitionOverwriteMode", output_conf['delta_options']['partition_overwrite_mode'])
        .option("mergeSchema", output_conf['delta_options']['merge_schema'])
        .option("overwriteSchema", output_conf['delta_options']['overwrite_schema'])
        .save(output_conf['delta_options']['location'])
    )


def write_delta_stream(spark_job_conf: dict, output_name: str, stream: DataFrame):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists(output_stream_conf, output_stream_conf['delta_options']['schema'])

    if output_stream_conf.get('processing_time') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(processingTime=output_stream_conf['processing_time']) \
            .partitionBy(output_stream_conf['delta_options']['partition_columns']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    elif output_stream_conf.get('availableNow') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(availableNow=output_stream_conf.get('availableNow')) \
            .partitionBy(output_stream_conf['delta_options']['partition_columns']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    elif output_stream_conf.get('once') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(once=output_stream_conf.get('once')) \
            .partitionBy(output_stream_conf['delta_options']['partition_columns']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    else:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .partitionBy(output_stream_conf['delta_options']['partition_columns']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])


def write_delta_stream_no_partitioning(spark_job_conf: dict, output_name: str, stream: DataFrame):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists_no_partitioning(output_stream_conf, output_stream_conf['delta_options']['schema'])

    if output_stream_conf.get('processing_time') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(processingTime=output_stream_conf['processing_time']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    elif output_stream_conf.get('availableNow') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(availableNow=output_stream_conf.get('availableNow')) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    elif output_stream_conf.get('once') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(once=output_stream_conf.get('once')) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])
    else:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start(output_stream_conf['delta_options']['location'])


def write_delta_stream_with_custom_fnc(spark_job_conf, output_name: str, stream: DataFrame, updater_function):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists_no_partitioning(output_stream_conf, output_stream_conf['delta_options']['schema'])

    if output_stream_conf.get('processing_time') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(processingTime=output_stream_conf['processing_time']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    elif output_stream_conf.get('availableNow') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(availableNow=output_stream_conf['availableNow']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    elif output_stream_conf.get('once') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(once=output_stream_conf['once']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    else:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()


def write_delta_stream_with_custom_fnc_same_foreach_batch(spark_job_conf: dict, output_name: str, stream: DataFrame,
                                                          updater_function):
    output_stream_conf = get_spark_conf(output_name, spark_job_conf['outputs'])
    # for output in output_stream_conf['delta_options']:
    #     DeltaTable \
    #         .createIfNotExists() \
    #         .addColumns(output['schema']) \
    #         .partitionedBy(output["partition_columns"]) \
    #         .location(output["location"]) \
    #         .execute()

    if output_stream_conf.get('processing_time') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(processingTime=output_stream_conf['processing_time']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    elif output_stream_conf.get('availableNow') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(availableNow=output_stream_conf['availableNow']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    elif output_stream_conf.get('once') is not None:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .trigger(once=output_stream_conf['once']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()
    else:
        stream \
            .writeStream \
            .queryName(output_stream_conf['name']) \
            .format("delta") \
            .outputMode(output_stream_conf['mode']) \
            .foreachBatch(updater_function) \
            .option("checkpointLocation", output_stream_conf['checkpoint_location']) \
            .option("mergeSchema", output_stream_conf['delta_options']['merge_schema']) \
            .option("overwriteSchema", output_stream_conf['delta_options']['overwrite_schema']) \
            .start()


########
# AVRO #
########
def get_register_avro_schema(kafka_deserialization_conf: dict) -> str:
    kafka_schema_registry_conf = {
        'url': kafka_deserialization_conf['kafka_schema_registry_url']
    }

    kafka_schema_registry_subject = kafka_deserialization_conf['kafka_schema_registry_subject_name']

    json_format_schema = SchemaRegistryClient(kafka_schema_registry_conf) \
        .get_latest_version(kafka_schema_registry_subject) \
        .schema \
        .schema_str

    return json_format_schema


def deserialize_register_avro_stream(stream: DataFrame, kafka_deserialization_conf: dict) -> DataFrame:
    from_avro_abris_settings = from_avro_abris_config({
        'schema.registry.url': kafka_deserialization_conf['schema.registry.url']
    }, kafka_deserialization_conf['topic'], False)

    deserialized_stream = stream \
        .withColumn("parsed", from_avro("value", from_avro_abris_settings)) \
        .select('parsed.*')

    return deserialized_stream


def serialize_register_avro_stream(stream: DataFrame, kafka_serialization_conf: dict) -> DataFrame:
    to_avro_abris_settings = to_avro_abris_config({
        'schema.registry.url': kafka_serialization_conf['schema.registry.url']
    }, kafka_serialization_conf['topic'], False)

    serialized_stream = stream \
        .select(to_avro(struct(stream.columns), to_avro_abris_settings).alias("value"))

    return serialized_stream


def from_avro(col, config):
    """
    avro deserialize

    :param col (PySpark column / str): column name "key" or "value"
    :param config (za.co.absa.abris.config.FromAvroConfig): abris config, generated from abris_config helper function
    :return: PySpark Column
    """
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    abris_avro = jvm_gateway.za.co.absa.abris.avro

    return Column(abris_avro.functions.from_avro(_to_java_column(col), config))


def from_avro_abris_config(config_map, topic, is_key):
    """
    Create from avro abris config with a schema url

    :param config_map (dict[str, str]): configuration map to pass to deserializer, ex: {'schema.registry.url': 'http://localhost:8081'}
    :param topic (str): kafka topic
    :param is_key (bool): boolean
    :return: za.co.absa.abris.config.FromAvroConfig
    """
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    scala_map = jvm_gateway.PythonUtils.toScalaMap(config_map)

    return jvm_gateway.za.co.absa.abris.config \
        .AbrisConfig \
        .fromConfluentAvro() \
        .downloadReaderSchemaByLatestVersion() \
        .andTopicNameStrategy(topic, is_key) \
        .usingSchemaRegistry(scala_map)


def to_avro(col, config):
    """
    avro serialize
    :param col (PySpark column / str): column name "key" or "value"
    :param config (za.co.absa.abris.config.ToAvroConfig): abris config, generated from abris_config helper function
    :return: PySpark Column
    """
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    abris_avro = jvm_gateway.za.co.absa.abris.avro

    return Column(abris_avro.functions.to_avro(_to_java_column(col), config))


def to_avro_abris_config(config_map, topic, is_key):
    """
    Create to avro abris config with a schema url

    :param config_map (dict[str, str]): configuration map to pass to the serializer, ex: {'schema.registry.url': 'http://localhost:8081'}
    :param topic (str): kafka topic
    :param is_key (bool): boolean
    :return: za.co.absa.abris.config.ToAvroConfig
    """
    jvm_gateway = SparkContext._active_spark_context._gateway.jvm
    scala_map = jvm_gateway.PythonUtils.toScalaMap(config_map)

    return jvm_gateway.za.co.absa.abris.config \
        .AbrisConfig \
        .toConfluentAvro() \
        .downloadSchemaByLatestVersion() \
        .andTopicNameStrategy(topic, is_key) \
        .usingSchemaRegistry(scala_map)


def instantiate_delta_table(spark_session: SparkSession, spark_job_conf: dict, table_name: str):
    table_conf = get_spark_conf(table_name, spark_job_conf['outputs'])
    create_delta_tables_if_not_exists(table_conf, table_conf['delta_options']['schema'])
    return DeltaTable.forPath(spark_session, table_conf['delta_options']['location'])


def instantiate_delta_tables(spark_session: SparkSession, spark_job_conf: dict, tables_name: str):
    tables_conf = get_spark_conf(tables_name, spark_job_conf['outputs'])

    results = dict()
    for table in tables_conf['delta_options']:
        DeltaTable \
            .createIfNotExists() \
            .addColumns(table['schema']) \
            .partitionedBy(table["partition_columns"]) \
            .location(table["location"]) \
            .execute()
        results[table['name']] = DeltaTable.forPath(spark_session, table['location'])

    return results

#######
# GA4 #
#######
def initialize_analytics_reporting(key_file_location):
    """
    Using a default constructor instructs the client to use the credentials
    specified in json file service account credentials.
    :param property_id: user base ID.
    :return: An authorized service object.
    """

    return BetaAnalyticsDataClient.from_service_account_file(key_file_location)


def print_run_report_response(response: RunReportResponse):
    """Prints results of a runReport call."""
    print(f"{response.row_count} rows received")
    for dimensionHeader in response.dimension_headers:
        print(f"Dimension header name: {dimensionHeader.name}")
    for metricHeader in response.metric_headers:
        metric_type = MetricType(metricHeader.type_).name
        print(f"Metric header name: {metricHeader.name} ({metric_type})")

    print("Report result:")
    for rowIdx, row in enumerate(response.rows):
        print(f"\nRow {rowIdx}")
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].name
            print(f"{dimension_name}: {dimension_value.value}")

        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            print(f"{metric_name}: {metric_value.value}")


def print_run_pivot_report_response(response):
    """Prints results of a runPivotReport call."""
    print("Report result:")
    for row in response.rows:
        for dimension_value in row.dimension_values:
            print(dimension_value.value)

        for metric_value in row.metric_values:
            print(metric_value.value)


def print_get_metadata_response(response):
    for dimension in response.dimensions:
        print("DIMENSION")
        print(f"{dimension.api_name} ({dimension.ui_name}): {dimension.description}")
        print(f"custom_definition: {dimension.custom_definition}")
        if dimension.deprecated_api_names:
            print(f"Deprecated API names: {dimension.deprecated_api_names}")
        print("")

    for metric in response.metrics:
        print("METRIC")
        print(f"{metric.api_name} ({metric.ui_name}): {metric.description}")
        print(f"custom_definition: {metric.custom_definition}")
        if metric.expression:
            print(f"Expression: {metric.expression}")

        metric_type = MetricType(metric.type_).name
        print(f"Type: {metric_type}")

        if metric.deprecated_api_names:
            print(f"Deprecated API names: {metric.deprecated_api_names}")
        print("")


def convert_to_pyspark_df(spark, responses):
    data = []
    for response in responses:
        for row in response.rows:
            row_data = [dimension.value for dimension in row.dimension_values]
            row_data.extend([metric.value for metric in row.metric_values])
            data.append(row_data)

    dimension_names = [dimension.name for dimension in responses[0].dimension_headers]
    metric_names = [metric.name for metric in responses[0].metric_headers]

    rows = [Row(**dict(zip(dimension_names + metric_names, row))) for row in data]

    if rows:
        return spark.createDataFrame(rows)
    else:
        return None


def convert_to_pyspark_df_without_pagination(spark, response):
    data = []
    for row in response.rows:
        row_data = [dimension.value for dimension in row.dimension_values]
        row_data.extend([metric.value for metric in row.metric_values])
        data.append(row_data)

    dimension_names = [dimension.name for dimension in response.dimension_headers]
    metric_names = [metric.name for metric in response.metric_headers]

    rows = [Row(**dict(zip(dimension_names + metric_names, row))) for row in data]

    if rows:
        return spark.createDataFrame(rows)
    else:
        return None

def convert_to_pyspark_df_total_only(spark, responses):
    data = []
    for response in responses:
        for row in response.totals:
            row_data = [dimension.value for dimension in row.dimension_values]
            row_data.extend([metric.value for metric in row.metric_values])
            data.append(row_data)

    dimension_names = [dimension.name for dimension in responses[0].dimension_headers]
    metric_names = [metric.name for metric in responses[0].metric_headers]

    if not any(data):
        # Create Empty dataframe
        schema = StructType([StructField(name, StringType(), True) for name in (dimension_names + metric_names)])
        row = Row(**dict(zip(dimension_names + metric_names, [None] * len(dimension_names + metric_names))))
        return spark.createDataFrame([row], schema=schema)
    else:
        rows = [Row(**dict(zip(dimension_names + metric_names, row))) for row in data]
        return spark.createDataFrame(rows)


class GoogleAnalytics:

    def __init__(self, property_id: str, key_file_location: str, spark: SparkSession):
        self.spark = spark
        self.property_id = str(int(property_id))
        self.key_file_location = key_file_location
        self.client = initialize_analytics_reporting(key_file_location)

    def get_metadata_by_property_id(self):

        request = GetMetadataRequest(name=f"properties/{self.property_id}/metadata")
        response = self.client.get_metadata(request)

        # print(
        #     f"Dimensions and metrics available for Google Analytics 4 "
        #     f"property {property_id} (including custom fields):"
        # )
        # print_get_metadata_response(response)

    def run_batch_report(self, requests: [RunReportRequest]):
        requests = BatchRunReportsRequest(
            property=f"properties/{self.property_id}",
            requests=requests
        )

        response = self.client.batch_run_reports(requests)

        return response

    def run_realtime_report(self,
                            dimensions: [Dimension],
                            metrics: [Metric],
                            dimension_filter: FilterExpression,
                            metric_filter: FilterExpression,
                            order_bys: [OrderBy],
                            metric_aggregations: [MetricAggregation],
                            limit=10000,
                            ):

        request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=dimensions,
            metrics=metrics,
            # date_ranges=date_ranges,
            dimension_filter=dimension_filter,
            metric_filter=metric_filter,
            limit=limit,
            # offset=offset,
            order_bys=order_bys,
            metric_aggregations=metric_aggregations
        )

        response = self.client.run_realtime_report(request)

        spark_df = convert_to_pyspark_df_without_pagination(self.spark, response)

        return spark_df

    def run_realtime_report_with_minute_ranges(
            self,
            dimensions: [Dimension],
            metrics: [Metric],
            dimension_filter: FilterExpression,
            metric_filter: FilterExpression,
            order_bys: [OrderBy],
            metric_aggregations: [MetricAggregation],
            minute_ranges: [MinuteRange],
            limit=10000
    ):
        request = RunRealtimeReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=dimensions,
            metrics=metrics,
            # date_ranges=date_ranges,
            dimension_filter=dimension_filter,
            metric_filter=metric_filter,
            limit=limit,
            # offset=offset,
            order_bys=order_bys,
            metric_aggregations=metric_aggregations,
            minute_ranges=minute_ranges
        )

        response = self.client.run_realtime_report(request)

        spark_df = convert_to_pyspark_df_without_pagination(self.spark, response)

        return spark_df

    def run_report(self,
                   dimensions: [Dimension],
                   metrics: [Metric],
                   date_ranges: [DateRange],
                   dimension_filter: FilterExpression,
                   metric_filter: FilterExpression,
                   order_bys: [OrderBy],
                   metric_aggregations: [MetricAggregation],
                   limit=100000,
                   offset=0,
                   hard_limit=False
                   ):

        responses = []
        while True:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=dimensions,
                metrics=metrics,
                date_ranges=date_ranges,
                dimension_filter=dimension_filter,
                metric_filter=metric_filter,
                limit=limit,
                offset=offset,
                order_bys=order_bys,
                metric_aggregations=metric_aggregations
            )

            response = self.client.run_report(request)

            responses.append(response)

            if hard_limit:
                break

            if offset + len(response.rows) >= response.row_count:
                break
            else:
                print(f'{offset} / {response.row_count}')
                offset += limit

        if metric_aggregations:
            if metric_aggregations[0] == MetricAggregation.TOTAL:
                return convert_to_pyspark_df_total_only(self.spark, responses)
        else:
            return convert_to_pyspark_df(self.spark, responses)

    def run_pivot_report(
            self,
            dimensions: [Dimension],
            metrics: [Metric],
            date_ranges: [DateRange],
            pivots: [Pivot],
            dimension_filter: FilterExpression,
            metric_filter: FilterExpression,
    ):

        request = RunPivotReportRequest(
            property=f"properties/{self.property_id}",
            dimensions=dimensions,
            metrics=metrics,
            date_ranges=date_ranges,
            pivots=pivots,
            dimension_filter=dimension_filter,
            metric_filter=metric_filter
        )

        response = self.client.run_pivot_report(request)

        return response