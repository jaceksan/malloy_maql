with carriers as (
  select * from {{ var("input_schema") }}.carriers
)
select * from carriers
