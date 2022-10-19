with aircraft_models as (
  select * from {{ var("input_schema") }}.aircraft_models
)
select * from aircraft_models
