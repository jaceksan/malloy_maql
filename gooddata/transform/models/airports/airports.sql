with airports as (
  select
    a.*,
    a.code || '-' || a.full_name as name
  from {{ var("input_schema") }}.airports a
)
select * from airports
