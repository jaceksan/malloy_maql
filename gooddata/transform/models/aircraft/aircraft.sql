with aircraft as (
  select * from {{ var("input_schema") }}.aircraft
)
select * from aircraft
