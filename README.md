# Eurobase Metadata Quality Framework (EMQF)

## Overview

EMQF is a Databricks-based metadata quality monitoring framework for Eurostat/Eurobase datasets. The platform ingests public metadata APIs, applies rule-based validation checks, calculates quality scores, and stores historical monitoring results using Delta Lake.

**Eurobase Metadata Quality Framework (EMQF)** is an automated metadata quality monitoring and validation framework for Eurostat/Eurobase datasets, built with **Databricks**, **PySpark**, **Delta Lake**, and public Eurostat APIs.

The project implements a Lakehouse-style data quality pipeline that ingests Eurostat metadata, enriches it with external catalogue information, applies rule-based validation checks, calculates dataset-level quality scores, and persists historical results for monitoring and analytics.

---

# High-Level Architecture

<img width="2055" height="1272" alt="emqf_architecture" src="https://github.com/user-attachments/assets/5b8be84b-f24e-4802-ae8f-fe6ff127f2a9" />

---

# Project Objective

The goal of EMQF is to automate metadata quality assessment for datasets updated in Eurostat/Eurobase and provide a repeatable, scalable framework for daily quality monitoring.

The framework answers questions such as:

- Which datasets were updated today?
- Do updated datasets follow metadata quality rules?
- Which datasets fail specific quality checks?
- How does metadata quality evolve over time?
- Which quality dimensions require attention?

---

# Data Sources

| Source | Purpose |
|---|---|
| Eurostat Table of Contents XML | Detect updated datasets and extract metadata fields |
| Eurostat SPARQL catalogue | Retrieve DOI and landing page information |
| Eurostat metabase | Retrieve dataset dimensions and codelist metadata |
| Eurostat SDMX APIs | Validate dimensional, aggregate, and confidentiality rules |
| ESA 2010 abbreviations page | Validate acronyms used in dataset titles |

---

# Lakehouse Flow

```text
Eurostat APIs
    ↓
Raw / Source Ingestion
    ↓
Metadata Enrichment
    ↓
Rule-Based Quality Checks
    ↓
Dataset-Level Quality Scores
    ↓
Delta Lake History + Latest Snapshot
    ↓
Databricks SQL / Dashboarding
```

## Implemented Quality Checks

| # | Check | Description |
|---|---|---|
| 1 | Metadata File Existence | Checks whether ESMS metadata exists |
| 2 | DOI Verification | Validates DOI availability from catalogue metadata |
| 3 | OP Dataset Availability | Checks availability of landing page / dissemination page |
| 4 | Data Browser Verification | Validates accessibility in Eurostat Data Browser |
| 5 | Source of Data Validation | Checks source formatting, Eurostat ordering, and acronym rules |
| 6 | Dataset Title Standards Verification | Applies title quality rules including length, acronyms, periodicity, units, and uniqueness |
| 7 | Validation of Historical Data Listing | Checks historical dataset title consistency using dataStart and dataEnd |
| 8 | Dimensional Completeness | Validates required dimension groups such as time, geo, and unit with domain-specific exceptions |
| 9 | Standard Codelists Percentage | Calculates percentage of standard codelists used by each dataset |
| 10 | EA20 Aggregate Consistency | Validates EA20 / EA19 aggregate consistency logic |
| 11 | EU27 Confidentiality Consistency | Checks EU27 aggregate confidentiality flag consistency for NACE-based datasets |

## Output Tables

| Table | Description |
|---|---|
| `emqa_daily_updated_datasets` | Datasets updated in the current run |
| `emqa_daily_datasets_enriched` | Daily datasets enriched with SPARQL catalogue metadata |
| `emqa_dimensions_metadata` | Enriched dimension and codelist metadata |
| `emqa_daily_quality_checks` | Dataset-level results for all quality checks |
| `emqa_daily_quality_score_history` | Historical daily quality scores, appended by run |
| `emqa_daily_quality_score_latest` | Latest quality score snapshot |

## Scheduling

The pipeline is designed to run through **Databricks Workflows**.

Recommended schedule:

```text
Monday to Friday at 11:01 Europe/Athens time
```

Quartz cron expression:

```text
0 1 11 ? * MON-FRI
```

## Final Scoring Logic

Each dataset receives a final quality score calculated as the average of implemented quality check scores.

The final output includes:

- `final_quality_score`
- `failed_conditions`
- `run_date`
- `run_timestamp`

## Technology Stack

| Area | Technology / Approach |
|---|---|
| Data Platform | Databricks |
| Processing | PySpark, Python, Pandas |
| Storage | Delta Lake |
| Orchestration | Databricks Workflows |
| APIs | Eurostat Dissemination API, SDMX API, SPARQL |
| Querying | Spark SQL / Databricks SQL |
| Governance & Validation | Automated metadata quality validation based on Eurostat dissemination guidelines, SDMX metadata structures, codelist conventions, and statistical metadata quality rules |

## Technical Highlights

- Automated ingestion from multiple Eurostat public APIs
- Lakehouse-style architecture using Delta Lake
- Incremental daily metadata processing
- Rule-based metadata quality validation engine
- Historical quality score tracking and monitoring
- Hybrid Spark + Pandas processing pipeline
- Scheduled weekday orchestration with Databricks Workflows
- Standards-aware validation using SDMX metadata structures and Eurostat dissemination conventions
- Reusable framework design for extensible metadata quality checks

## Scalability & Engineering Considerations

The framework was designed with scalability and extensibility in mind:

- Delta Lake persistence for historical monitoring
- Incremental processing of only updated datasets
- Separation between latest snapshot and historical tables
- Parallel API retrieval for aggregate consistency checks
- Modular quality-check architecture for future rule expansion
- Databricks Workflow orchestration for automated execution
- Designed to support future migration from Pandas-heavy logic to Spark-native distributed transformations

## Metadata Governance Basis

The validation framework incorporates publicly available Eurostat and SDMX metadata conventions, including:

- dissemination metadata structures
- codelist standardization practices
- dataset title formatting conventions
- aggregate consistency validation logic
- confidentiality flag consistency checks
- metadata quality monitoring principles

The framework translates these governance-oriented rules into automated validation checks and quality scoring logic.

## Future Enhancements

- Refactor notebook logic into reusable Python modules
- Move more Pandas logic to Spark-native transformations
- Add structured logging and runtime metrics
- Create a pipeline execution metrics table
- Add unit tests for validation rules
- Build Databricks SQL dashboards
- Add CI/CD for notebook deployment
- Implement Delta MERGE logic for idempotent history writes

## Current Status

The framework is currently implemented as a Databricks notebook-based pipeline with scheduled weekday execution and Delta Lake persistence. The architecture is designed to support future modularization into reusable Python packages and Spark-native distributed processing components.

## Screenshots

![Workflow](screenshots/workflow.png)

![Quality Scores](screenshots/final_scores.png)
