with ranked as (

    select *,
           row_number() over (
               partition by dataset_code
               order by run_date desc, run_timestamp desc
           ) as rn
    from {{ ref('stg_emqf_quality_score_history') }}

)

select
    dataset_code,
    domain_acronym,
    top_theme,
    final_quality_score,
    run_date,
    run_timestamp
from ranked
where rn = 1
