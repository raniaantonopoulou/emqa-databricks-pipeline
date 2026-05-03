# Data Quality Monitoring Pipeline (Databricks & PySpark)

> Developed in Databricks using PySpark (notebook exported as .py for version control)

---

## 📌 Overview

This project implements a scalable **data quality monitoring pipeline** inspired by real-world statistical data validation workflows.

It processes public Eurostat metadata and applies automated validation rules, producing dataset-level quality scores and reporting-ready outputs.

This project demonstrates how data quality validation can be automated at scale using distributed data processing.

The pipeline follows a modern **Lakehouse architecture (Bronze-Silver-Gold)**.

---

## 🏗️ Architecture

### 🥉 Bronze Layer — Data Ingestion

* Ingests raw metadata from Eurostat public TOC API
* Stores unprocessed data
* Adds ingestion metadata (timestamp, source)

---

### 🥈 Silver Layer — Transformation

* Cleans and standardizes dataset metadata
* Filters valid datasets
* Creates dataset-level indicators:

  * Update availability
  * Dataset classification
  * NACE-related metadata detection

---

### 🔍 Data Quality Checks

* Validates dataset completeness:

  * Missing dataset codes
  * Missing titles
  * Missing update dates
  * Missing data ranges
* Flags datasets that fail validation rules

---

### 🥇 Gold Layer — Quality Scoring

* Computes dataset-level quality scores (0–100)
* Aggregates validation results
* Produces reporting-ready tables

---

### 📊 Reporting Layer

* Identifies low-quality datasets
* Aggregates quality scores by dataset family
* Provides summary metrics for monitoring

---

## ⚙️ Technologies

* PySpark
* Databricks (Community Edition)
* Delta Lake
* REST API ingestion

---

## ⭐ Key Features

* End-to-end data pipeline using PySpark
* Bronze-Silver-Gold architecture
* Automated data validation framework
* Dataset-level quality scoring
* Modular pipeline design

---

## 📈 Example Outputs

* Dataset quality scores
* Failed validation datasets
* Overall quality metrics
* Quality distribution by dataset group

---

## 🔄 Pipeline Execution

The pipeline includes structured steps:

1. Data ingestion (API)
2. Data transformation
3. Validation checks
4. Quality scoring
5. Reporting output generation

---

## 🚀 Improvements & Future Work

* Incremental data processing (process only updated datasets)
* Rule-based validation engine for flexible checks
* Alerting system for failed datasets
* Integration with dashboard tools (e.g. Power BI)
* Pipeline orchestration (scheduled execution)

---

## 📁 Project Structure

```
databricks-data-quality-pipeline/
 ├── README.md
 ├── mini_emqa_pipeline.py
```

---

## ⚠️ Note

This is a **portfolio project inspired by production data quality pipelines**.

* Uses only public datasets
* Does not include any private or internal data
* Designed to demonstrate scalable data engineering practices

---

## 👩‍💻 Author

Rania Antonopoulou
Data Engineer | Data Analytics Engineer
