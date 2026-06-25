# EMQF Architecture

```text
                    Azure Data Factory
                           │
                           ▼
                  Azure Databricks
                           │
                           ▼
                EMQF Quality Processing
                           │
                           ▼
         Snowflake Data Warehouse (Star Schema)
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
DIM_DATASET         DIM_DOMAIN           DIM_DATE
      │                    │                    │
      └──────────────┬─────┴────────────────────┘
                     ▼
            FACT_QUALITY_SCORE
                     │
                     ▼
          FACT_QUALITY_CHECK_RESULT
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
DOMAIN_HEALTH   SCORE_CHANGES   SLA_STATUS
                     │
                     ▼
                  ALERTS
```
