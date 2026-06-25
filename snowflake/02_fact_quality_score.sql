-- =====================================================
-- EMQF Snowflake Data Warehouse
-- Fact Table: Quality Score History
-- =====================================================

CREATE OR REPLACE TABLE EMQF.QUALITY.FACT_QUALITY_SCORE AS
SELECT
    ds.DATASET_KEY,
    dd.DOMAIN_KEY,
    dt.DATE_KEY,
    h.DATASET_CODE,
    h.DOMAIN_ACRONYM,
    h.RUN_DATE,
    h.RUN_TIMESTAMP,
    h.FINAL_QUALITY_SCORE
FROM EMQF.QUALITY.EMQF_QUALITY_SCORE_HISTORY h

LEFT JOIN EMQF.QUALITY.DIM_DATASET ds
    ON h.DATASET_CODE = ds.DATASET_CODE

LEFT JOIN EMQF.QUALITY.DIM_DOMAIN dd
    ON h.DOMAIN_ACRONYM = dd.DOMAIN_ACRONYM

LEFT JOIN EMQF.QUALITY.DIM_DATE dt
    ON h.RUN_DATE = dt.RUN_DATE;
