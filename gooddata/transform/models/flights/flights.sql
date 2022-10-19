with flights as (
  select * from {{ var("input_schema") }}.flights
)
select * from flights
