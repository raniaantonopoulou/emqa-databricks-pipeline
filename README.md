# Data Quality Monitoring Pipeline (Databricks & PySpark)

## Overview
This project implements a data quality monitoring pipeline inspired by real-world statistical data validation workflows.

The pipeline follows a Bronze-Silver-Gold architecture and processes public Eurostat metadata to detect quality issues and generate dataset-level scores.

## Architecture

- **Bronze Layer**
  - Ingests raw data from Eurostat public TOC API
  - Stores metadata without transformation

- **Silver Layer**
  - Cleans and standardizes dataset metadata
  - Filters valid datasets
  - Creates dataset-level indicators (e.g., update status, NACE relevance)

- **Quality Checks**
  - Validates dataset metadata completeness
  - Checks for missing dataset codes, titles, and update information
  - Flags datasets failing validation rules

- **Gold Layer**
  - Computes data quality scores per dataset
  - Produces summary metrics for reporting

- **Reporting Layer**
  - Identifies low-quality datasets
  - Aggregates quality scores by dataset category

## Technologies

- PySpark
- Databricks (Community Edition)
- Delta Lake
- REST API ingestion

## Key Features

- Automated data ingestion from public API
- Data validation framework (EMQA-inspired)
- Dataset-level quality scoring
- Scalable Spark-based transformations
- Reporting-ready output tables

## Example Outputs

- Dataset quality scores (0–100)
- Overall quality metrics
- Quality breakdown by dataset group

## How to Run

1. Open notebook in Databricks Community Edition
2. Run cells sequentially (01 → 07)
3. Tables will be created automatically:
   - bronze_toc
   - silver_toc
   - silver_quality_checks
   - gold_quality_scores
   - gold_quality_summary

## Note

This project is a portfolio version inspired by production data quality pipelines.
It uses only public data and does not include any private or internal sources.
