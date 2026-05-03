# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Setup
# MAGIC
# MAGIC This notebook builds a mini data quality monitoring pipeline using Databricks and PySpark.
# MAGIC It follows a Bronze-Silver-Gold architecture:
# MAGIC - Bronze: Raw data ingestion
# MAGIC - Silver: Cleaned and validated data
# MAGIC - Gold: Aggregated results and quality scoring

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit

spark = SparkSession.builder.getOrCreate()

print("Spark session started successfully")

# COMMAND ----------

bronze_table = "bronze_toc"
silver_table = "silver_toc"
gold_table = "gold_quality_scores"

print("Tables initialized:")
print(bronze_table, silver_table, gold_table)

# COMMAND ----------

bronze_table = "bronze_toc"
silver_table = "silver_toc"
gold_table = "gold_quality_scores"

print("Tables initialized:")
print(bronze_table, silver_table, gold_table)

# COMMAND ----------

# MAGIC %md
# MAGIC # 02 - Data Ingestion (Bronze Layer)
# MAGIC
# MAGIC This step ingests public Eurostat catalogue metadata from the public TOC API.
# MAGIC The data is stored as raw Bronze data without transformations.

# COMMAND ----------

import requests
import xml.etree.ElementTree as ET
from pyspark.sql import Row
from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.types import StructType, StructField, StringType

# COMMAND ----------

toc_url = "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/xml"

response = requests.get(toc_url)
response.raise_for_status()

root = ET.fromstring(response.content)

namespace = "{urn:eu.europa.ec.eurostat.navtree}"

# COMMAND ----------

records = []

def extract_toc(element):
    title = element.find(f"{namespace}title")
    code = element.find(f"{namespace}code")
    last_update = element.find(f"{namespace}lastUpdate")
    last_modified = element.find(f"{namespace}lastModified")
    data_start = element.find(f"{namespace}dataStart")
    data_end = element.find(f"{namespace}dataEnd")

    if code is not None:
        inferred_type = "dataset" if (
            last_update is not None or data_start is not None or data_end is not None
        ) else "folder"

        records.append(Row(
            title=title.text if title is not None else None,
            Dataset_Code=code.text if code is not None else None,
            type=inferred_type,
            last_update=last_update.text if last_update is not None else None,
            last_modified=last_modified.text if last_modified is not None else None,
            data_start=data_start.text if data_start is not None else None,
            data_end=data_end.text if data_end is not None else None
        ))

    for child in element:
        extract_toc(child)

extract_toc(root)

# COMMAND ----------

toc_schema = StructType([
    StructField("title", StringType(), True),
    StructField("Dataset_Code", StringType(), True),
    StructField("type", StringType(), True),
    StructField("last_update", StringType(), True),
    StructField("last_modified", StringType(), True),
    StructField("data_start", StringType(), True),
    StructField("data_end", StringType(), True)
])

bronze_toc_df = spark.createDataFrame(records, schema=toc_schema)

# COMMAND ----------

bronze_toc_df = (
    bronze_toc_df
    .withColumn("source_system", lit("Eurostat public TOC API"))
    .withColumn("ingestion_timestamp", current_timestamp())
)

display(bronze_toc_df)

# COMMAND ----------

bronze_toc_df.write.mode("overwrite").format("delta").saveAsTable(bronze_table)

print("Bronze TOC table saved successfully")

# COMMAND ----------

display(spark.table(bronze_table))

# COMMAND ----------

# MAGIC %md
# MAGIC # 03 - Data Filtering and Transformation (Silver Layer)
# MAGIC
# MAGIC This step cleans the raw Eurostat catalogue data and creates a Silver table with dataset-level indicators.
# MAGIC It follows the same idea as the EMQA pipeline: prepare metadata before running validation checks.

# COMMAND ----------

from pyspark.sql.functions import (
    col, lower, trim, coalesce, lit, when, to_date, split, element_at
)

# COMMAND ----------

bronze_toc_df = spark.table(bronze_table)

display(bronze_toc_df)

# COMMAND ----------

silver_toc_df = (
    bronze_toc_df
    .withColumn("Dataset_Code", trim(col("Dataset_Code")))
    .withColumn("title", trim(col("title")))
    .withColumn("type", coalesce(trim(col("type")), lit("folder")))
    .withColumn(
        "last_update_date",
        coalesce(
            to_date(col("last_update"), "dd.MM.yyyy"),
            to_date(col("last_update"), "yyyy-MM-dd")
        )
    )
    .withColumn(
        "last_modified_date",
        coalesce(
            to_date(col("last_modified"), "dd.MM.yyyy"),
            to_date(col("last_modified"), "yyyy-MM-dd")
        )
    )
)

display(silver_toc_df)

# COMMAND ----------

silver_toc_df = (
    silver_toc_df
    .filter(lower(col("type")) == "dataset")
    .dropDuplicates(["Dataset_Code"])
)

display(silver_toc_df)

# COMMAND ----------

silver_toc_df = (
    silver_toc_df
    .withColumn("dataset_family", element_at(split(col("Dataset_Code"), "_"), 1))
    .withColumn(
        "Has_Nace_Candidate",
        when(
            lower(col("title")).contains("nace") |
            lower(col("title")).contains("economic activity") |
            lower(col("Dataset_Code")).contains("nace"),
            lit(True)
        ).otherwise(lit(False))
    )
    .withColumn(
        "Is_Updated",
        when(col("last_update_date").isNotNull(), lit(True)).otherwise(lit(False))
    )
)

display(silver_toc_df)

# COMMAND ----------

silver_toc_df.write.mode("overwrite").format("delta").saveAsTable(silver_table)

print("Silver TOC table saved successfully")

# COMMAND ----------

display(spark.table(silver_table))

# COMMAND ----------

# MAGIC %md
# MAGIC # 04 - Data Quality Checks
# MAGIC
# MAGIC This step applies EMQA-style validation checks on the Silver metadata table.
# MAGIC The goal is to detect metadata quality issues before scoring.

# COMMAND ----------

from pyspark.sql.functions import col, when, lit, count, sum as spark_sum

# COMMAND ----------

silver_toc_df = spark.table(silver_table)

display(silver_toc_df)

# COMMAND ----------

quality_checks_df = (
    silver_toc_df
    .withColumn(
        "Check_Has_Dataset_Code",
        when(col("Dataset_Code").isNotNull() & (col("Dataset_Code") != ""), lit(True))
        .otherwise(lit(False))
    )
    .withColumn(
        "Check_Has_Title",
        when(col("title").isNotNull() & (col("title") != ""), lit(True))
        .otherwise(lit(False))
    )
    .withColumn(
        "Check_Has_Update_Date",
        when(col("last_update_date").isNotNull(), lit(True))
        .otherwise(lit(False))
    )
    .withColumn(
        "Check_Has_Data_Range",
        when(col("data_start").isNotNull() | col("data_end").isNotNull(), lit(True))
        .otherwise(lit(False))
    )
)

display(quality_checks_df)

# COMMAND ----------

quality_checks_df = (
    quality_checks_df
    .withColumn(
        "Metadata_Quality_Check",
        when(
            col("Check_Has_Dataset_Code")
            & col("Check_Has_Title")
            & col("Check_Has_Update_Date"),
            lit(True)
        ).otherwise(lit(False))
    )
)

display(quality_checks_df)

# COMMAND ----------

quality_summary_df = quality_checks_df.select(
    count("*").alias("total_datasets"),
    spark_sum(when(col("Check_Has_Dataset_Code") == False, 1).otherwise(0)).alias("missing_dataset_code"),
    spark_sum(when(col("Check_Has_Title") == False, 1).otherwise(0)).alias("missing_title"),
    spark_sum(when(col("Check_Has_Update_Date") == False, 1).otherwise(0)).alias("missing_update_date"),
    spark_sum(when(col("Check_Has_Data_Range") == False, 1).otherwise(0)).alias("missing_data_range"),
    spark_sum(when(col("Metadata_Quality_Check") == False, 1).otherwise(0)).alias("failed_metadata_quality_check")
)

display(quality_summary_df)

# COMMAND ----------

quality_checks_table = "silver_quality_checks"

quality_checks_df.write.mode("overwrite").format("delta").saveAsTable(quality_checks_table)

print("Quality checks table saved successfully")

# COMMAND ----------

# MAGIC %md
# MAGIC # 05 - Quality Scoring (Gold Layer)
# MAGIC
# MAGIC This step creates reporting-ready quality score tables from the validation results.
# MAGIC The output can be used for dashboards or portfolio reporting.

# COMMAND ----------

from pyspark.sql.functions import col, when, lit, round, count, sum as spark_sum

# COMMAND ----------

quality_checks_df = spark.table("silver_quality_checks")

display(quality_checks_df)

# COMMAND ----------

gold_quality_scores_df = (
    quality_checks_df
    .withColumn(
        "passed_checks",
        when(col("Check_Has_Dataset_Code"), 1).otherwise(0)
        + when(col("Check_Has_Title"), 1).otherwise(0)
        + when(col("Check_Has_Update_Date"), 1).otherwise(0)
        + when(col("Check_Has_Data_Range"), 1).otherwise(0)
    )
    .withColumn("total_checks", lit(4))
    .withColumn(
        "quality_score",
        round((col("passed_checks") / col("total_checks")) * 100, 2)
    )
)

display(gold_quality_scores_df)

# COMMAND ----------

gold_summary_df = gold_quality_scores_df.select(
    count("*").alias("total_datasets"),
    round((spark_sum("passed_checks") / (count("*") * lit(4))) * 100, 2).alias("overall_quality_score"),
    spark_sum(when(col("Metadata_Quality_Check") == True, 1).otherwise(0)).alias("passed_datasets"),
    spark_sum(when(col("Metadata_Quality_Check") == False, 1).otherwise(0)).alias("failed_datasets")
)

display(gold_summary_df)

# COMMAND ----------

gold_quality_scores_df.write.mode("overwrite").format("delta").saveAsTable(gold_table)
gold_summary_df.write.mode("overwrite").format("delta").saveAsTable("gold_quality_summary")

print("Gold quality tables saved successfully")

# COMMAND ----------

display(spark.table(gold_table))
display(spark.table("gold_quality_summary"))

# COMMAND ----------

# MAGIC %md
# MAGIC # 06 - Reporting Outputs
# MAGIC
# MAGIC This step prepares final reporting views that can be used in dashboards or exported for analysis.

# COMMAND ----------

gold_quality_scores_df = spark.table(gold_table)
gold_summary_df = spark.table("gold_quality_summary")

# COMMAND ----------

display(
    gold_quality_scores_df
    .select("Dataset_Code", "title", "quality_score", "Metadata_Quality_Check")
    .orderBy(col("quality_score").asc())
)

# COMMAND ----------

from pyspark.sql.functions import avg, count, round

family_summary_df = (
    gold_quality_scores_df
    .groupBy("dataset_family")
    .agg(
        count("*").alias("total_datasets"),
        round(avg("quality_score"), 2).alias("average_quality_score")
    )
    .orderBy(col("average_quality_score").asc())
)

display(family_summary_df)

# COMMAND ----------

family_summary_df.write.mode("overwrite").format("delta").saveAsTable("gold_family_quality_summary")

print("Reporting output table saved successfully")

# COMMAND ----------

display(spark.table("gold_quality_summary"))
display(spark.table("gold_family_quality_summary"))

# COMMAND ----------

# MAGIC %md
# MAGIC # 07 - Project Conclusion
# MAGIC
# MAGIC This project demonstrates a mini data quality monitoring pipeline inspired by real-world EMQA-style validation workflows.
# MAGIC
# MAGIC The pipeline includes:
# MAGIC
# MAGIC - Public API ingestion from Eurostat
# MAGIC - Bronze-Silver-Gold architecture
# MAGIC - Dataset metadata cleaning
# MAGIC - Automated quality checks
# MAGIC - Dataset-level quality scoring
# MAGIC - Reporting-ready summary tables
# MAGIC
# MAGIC This portfolio version uses only public metadata and does not include private/internal data sources.

# COMMAND ----------

print("Mini EMQA Databricks pipeline completed successfully.")

display(spark.table("gold_quality_summary"))