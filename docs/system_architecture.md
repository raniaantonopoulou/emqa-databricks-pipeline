# EMQF System Architecture

## Overview

EMQF (Eurobase Metadata Quality Framework) is an Azure Databricks Lakehouse solution for automated metadata quality monitoring of Eurostat datasets.

The framework leverages Azure Data Lake Storage Gen2 (ADLS Gen2), Delta Lake and PySpark to ingest, validate, score and monitor metadata quality across Eurostat datasets.

---

# High-Level Architecture

Eurostat APIs
        ↓
Azure Databricks (PySpark)
        ↓
Raw Layer (ADLS Gen2)
        ↓
Silver Layer (ADLS Gen2)
        ↓
Validation Engine
        ↓
Quality Scoring
        ↓
Gold Layer (ADLS Gen2)
        ↓
Power BI / Monitoring  

---

# Processing Layers

## 1. Metadata Ingestion

Retrieves:
- Eurostat TOC metadata
- SDMX metadata
- SPARQL catalogue metadata
- dimensions and codelists

## 2. Metadata Enrichment

Enriches datasets with:
- DOI information
- landing pages
- dimensions
- codelists
- domain classification
- source institution metadata

## 3. Validation Engine

Implements automated metadata quality checks including:
- metadata existence
- DOI validation
- title validation
- dimensional completeness
- aggregate consistency
- confidentiality consistency

## 4. Quality Scoring

Calculates:
- dataset-level validation scores
- final quality scores
- failed validation conditions

## 5. Historical Monitoring

Stores:
- latest score snapshots
- historical quality monitoring
- domain-level quality tracking

---

# Main Delta Tables

| Table | Purpose |
|---|---|
| `emqf_daily_updated_datasets` | Daily updated datasets |
| `emqf_daily_datasets_enriched` | Enriched metadata |
| `emqf_dimensions_metadata` | Dimensions and codelists |
| `emqf_daily_quality_checks` | Validation results |
| `emqf_daily_quality_score_latest` | Latest quality scores |
| `emqf_daily_quality_score_history` | Historical quality monitoring |

---

# Workflow Orchestration

The pipeline runs through Databricks Workflows using scheduled execution and incremental processing of updated datasets.

---

# Engineering Notes

- Azure Databricks Lakehouse architecture
- Azure Data Lake Storage Gen2 (ADLS Gen2)
- Delta Lake persistence
- Raw / Silver / Gold architecture
- Hybrid Spark + Pandas processing
- GitHub-integrated development workflow
- Automated metadata quality monitoring
