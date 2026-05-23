# EMQF System Architecture

## Overview

EMQF (Eurobase Metadata Quality Framework) is a Databricks Lakehouse pipeline for automated metadata quality monitoring of Eurostat datasets.

The framework retrieves metadata from Eurostat APIs, applies validation rules, calculates quality scores, and stores historical monitoring results in Delta Lake tables.

---

# High-Level Architecture

Eurostat APIs  
↓  
Metadata Ingestion  
↓  
Metadata Enrichment  
↓  
Validation Engine  
↓  
Quality Scoring  
↓  
Delta Lake Storage  
↓  
Dashboard / Monitoring  

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

- Databricks Lakehouse architecture
- Delta Lake persistence
- Hybrid Spark + Pandas processing
- Parallel Eurostat API retrieval
- Metadata governance-oriented validation logic
- Historical quality score persistence
