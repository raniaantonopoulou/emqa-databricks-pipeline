# EMQF Snowflake Data Warehouse

## Overview

The EMQF (Eurobase Metadata Quality Framework) warehouse was designed to support metadata quality monitoring, trend analysis, SLA tracking and quality degradation detection across Eurostat datasets.

The solution combines:

- Azure Data Factory (orchestration)
- Azure Databricks (processing and transformations)
- Snowflake (data warehouse and monitoring layer)
- GitHub (version control)

---

## Architecture

```text
Azure Data Factory
          │
          ▼
Azure Databricks
          │
          ▼
EMQF Quality Score History
          │
          ▼
Snowflake Data Warehouse
          │
          ├── DIM_DATASET
          ├── DIM_DOMAIN
          ├── DIM_DATE
          ├── DIM_QUALITY_CHECK
          │
          ├── FACT_QUALITY_SCORE
          └── FACT_QUALITY_CHECK_RESULT
                    │
                    ▼
      Monitoring & Analytics Layer
          ├── EMQF_DOMAIN_HEALTH
          ├── EMQF_SCORE_CHANGES
          ├── EMQF_ALERTS
          └── EMQF_SLA_STATUS
```

---

## Dimensions

### DIM_DATASET
Contains dataset metadata and identifiers.

### DIM_DOMAIN
Contains Eurostat domain information.

### DIM_DATE
Supports trend and historical analysis.

### DIM_QUALITY_CHECK
Contains quality validation rules including:

- Metadata File Existence ESMS
- DOI Verification
- OP Dataset Availability
- Data Browser Verification
- Source of Data Validation
- Dataset Title Standards
- Historical Data Listing
- Dimensional Completeness
- Standard Codelists
- EA20 Aggregate Consistency
- EU27 Confidentiality

---

## Fact Tables

### FACT_QUALITY_SCORE

Stores the final quality score per dataset and execution date.

### FACT_QUALITY_CHECK_RESULT

Stores individual quality check scores, enabling:

- Quality degradation analysis
- SLA monitoring
- Check-level reporting
- Root cause analysis

---

## Monitoring Views

### EMQF_DOMAIN_HEALTH

Domain-level quality monitoring.

### EMQF_SCORE_CHANGES

Tracks score changes over time.

### EMQF_ALERTS

Detects significant score increases or decreases.

### EMQF_SLA_STATUS

Tracks compliance against quality thresholds.

---

## Business Value

The platform supports:

- Metadata quality monitoring
- Quality score trend analysis
- Early detection of quality degradation
- SLA reporting
- Domain-level quality governance
- Automated quality assessment analytics
