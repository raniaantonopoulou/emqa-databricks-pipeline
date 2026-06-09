# Azure Lakehouse Architecture

## Project Overview

The Eurobase Metadata Quality Framework (EMQF) has been extended with a cloud-based Lakehouse architecture using Azure services.

The framework automates metadata quality validation, KPI calculation, historical tracking, and reporting for Eurostat datasets.

## Technology Stack

- Azure Databricks
- Azure Data Lake Storage Gen2 (ADLS Gen2)
- Delta Lake
- PySpark
- GitHub
- Power BI (planned integration)

---

## Lakehouse Architecture

### Raw Layer

Stores source data exactly as received from Eurostat APIs.

Examples:

- toc_xml

### Silver Layer

Stores cleaned and transformed datasets used by quality validation processes.

Examples:

- emqf_daily_updated_datasets

### Gold Layer

Stores business-ready outputs, KPIs and historical monitoring tables.

Examples:

- emqf_daily_quality_score_history
- emqf_daily_quality_score_latest

---

## Data Flow

    Eurostat APIs
            ↓
    Azure Databricks (PySpark Processing)
            ↓
    ADLS Gen2 Raw Layer
            ↓
    ADLS Gen2 Silver Layer
            ↓
    ADLS Gen2 Gold Layer
            ↓
    Reporting & Analytics

---

## Implemented Features

- Automated metadata quality validation
- Daily KPI generation
- Historical quality score tracking
- Delta Lake storage format
- Azure Data Lake Storage Gen2 integration
- GitHub version-controlled development workflow

---

## Azure Components

### Azure Databricks

Used for data ingestion, transformation and quality validation workflows.

### Azure Data Lake Storage Gen2

Used as the persistent storage layer following a Raw / Silver / Gold architecture.

### Delta Lake

Provides ACID transactions, schema evolution and efficient storage for quality monitoring datasets.

---

## Portfolio Demonstration

The project demonstrates:

- Azure Databricks development
- Azure Data Lake Storage Gen2 integration
- Delta Lake implementation
- Lakehouse architecture design
- PySpark data engineering workflows
- Metadata quality monitoring at scale
