-- =====================================================
-- EMQF Snowflake Data Warehouse
-- Dimension Tables
-- =====================================================

CREATE OR REPLACE TABLE EMQF.QUALITY.DIM_DATE AS
SELECT DISTINCT
    TO_NUMBER(TO_CHAR(RUN_DATE,'YYYYMMDD')) AS DATE_KEY,
    RUN_DATE,
    YEAR(RUN_DATE) AS YEAR,
    MONTH(RUN_DATE) AS MONTH,
    WEEK(RUN_DATE) AS WEEK,
    DAYOFWEEK(RUN_DATE) AS DAY_OF_WEEK
FROM EMQF.QUALITY.EMQF_QUALITY_SCORE_HISTORY
WHERE RUN_DATE IS NOT NULL;


CREATE OR REPLACE TABLE EMQF.QUALITY.DIM_DOMAIN AS
SELECT
    ROW_NUMBER() OVER (ORDER BY DOMAIN_ACRONYM) AS DOMAIN_KEY,
    DOMAIN_ACRONYM,
    TOP_THEME
FROM (
    SELECT DISTINCT
        DOMAIN_ACRONYM,
        TOP_THEME
    FROM EMQF.QUALITY.EMQF_QUALITY_SCORE_HISTORY
);


CREATE OR REPLACE TABLE EMQF.QUALITY.DIM_DATASET AS
SELECT
    ROW_NUMBER() OVER (ORDER BY DATASET_CODE) AS DATASET_KEY,
    DATASET_CODE,
    DOMAIN_ACRONYM,
    TOP_THEME
FROM (
    SELECT DISTINCT
        DATASET_CODE,
        DOMAIN_ACRONYM,
        TOP_THEME
    FROM EMQF.QUALITY.EMQF_QUALITY_SCORE_HISTORY
);


CREATE OR REPLACE TABLE EMQF.QUALITY.DIM_QUALITY_CHECK (
    CHECK_KEY NUMBER,
    CHECK_NAME STRING,
    CHECK_CATEGORY STRING
);


INSERT INTO EMQF.QUALITY.DIM_QUALITY_CHECK VALUES
(1,'Metadata File Existence ESMS','Metadata'),
(2,'DOI Verification','Metadata'),
(3,'OP Dataset Availability','Availability'),
(4,'Data Browser Verification','Availability'),
(5,'Source of Data Validation','Metadata'),
(6,'Dataset Title Standards','Metadata'),
(7,'Historical Data Listing','Consistency'),
(8,'Dimensional Completeness','Structure'),
(9,'Standard Codelists','Structure'),
(10,'EA20 Aggregate Consistency','Aggregation'),
(11,'EU27 Confidentiality','Confidentiality');
