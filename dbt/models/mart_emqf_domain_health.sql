select
    domain_acronym,
    count(*) as datasets,
    round(avg(final_quality_score),2) as avg_quality_score,
    min(final_quality_score) as min_quality_score,
    max(final_quality_score) as max_quality_score
from {{ ref('mart_emqf_latest_quality') }}
group by domain_acronym
order by avg_quality_score desc
