create table "aircraft_models"(
  "aircraft_model_code" varchar,
  "manufacturer" varchar,
  "model" varchar,
  "aircraft_type_id" int,
  "aircraft_engine_type_id" int,
  "aircraft_category_id" int,
  "amateur" int,
  "engines" int,
  "seats" int,
  "weight" int,
  "speed" int,
  constraint "pk_aircraft_models" primary key ("aircraft_model_code")
);
