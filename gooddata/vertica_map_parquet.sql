create schema if not exists faa;
set search_path to faa,public;

-----------------------------------------------------------------------------------------------------------------------------------

-- SELECT INFER_TABLE_DDL(
--          '/data/faa/carriers.parquet'
--            USING PARAMETERS format = 'parquet', table_name = 'carriers', table_type = 'external'
--          );

create external table "carriers"(
  "code" varchar,
  "name" varchar,
  "nickname" varchar
) as copy from '/data/faa/carriers.parquet' parquet;

alter table carriers add constraint pk_carriers primary key (code);

-----------------------------------------------------------------------------------------------------------------------------------

-- SELECT INFER_TABLE_DDL(
--          '/data/faa/airports.parquet'
--            USING PARAMETERS format = 'parquet', table_name = 'airports', table_type = 'external'
--          );

create external table "public"."airports"(
   "id" int,
   "code" varchar,
   "site_number" varchar,
   "fac_type" varchar,
   "fac_use" varchar,
   "faa_region" varchar,
   "faa_dist" varchar,
   "city" varchar,
   "county" varchar,
   "state" varchar,
   "full_name" varchar,
   "own_type" varchar,
   "longitude" float,
   "latitude" float,
   "elevation" int,
   "aero_cht" varchar,
   "cbd_dist" int,
   "cbd_dir" varchar,
   "act_date" varchar,
   "cert" varchar,
   "fed_agree" varchar,
   "cust_intl" varchar,
   "c_ldg_rts" varchar,
   "joint_use" varchar,
   "mil_rts" varchar,
   "cntl_twr" varchar,
   "major" varchar
) as copy from '/data/faa/airports.parquet' parquet;

create table airports as select a.*, code || '-' || full_name as name from public.airports a;

alter table airports add constraint pk_airports primary key (code);

-----------------------------------------------------------------------------------------------------------------------------------

-- SELECT INFER_TABLE_DDL(
--          '/data/faa/aircraft_models.parquet'
--            USING PARAMETERS format = 'parquet', table_name = 'aircraft_models', table_type = 'external'
--          );

create external table "aircraft_models"(
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
  "speed" int
) as copy from '/data/faa/aircraft_models.parquet' parquet;

alter table aircraft_models add constraint pk_aircraft_models primary key (aircraft_model_code);

-----------------------------------------------------------------------------------------------------------------------------------

-- SELECT INFER_TABLE_DDL(
--          '/data/faa/aircraft.parquet'
--            USING PARAMETERS format = 'parquet', table_name = 'aircraft', table_type = 'external'
--          );

create external table "aircraft"(
  "id" int,
  "tail_num" varchar,
  "aircraft_serial" varchar,
  "aircraft_model_code" varchar,
  "aircraft_engine_code" varchar,
  "year_built" int,
  "aircraft_type_id" int,
  "aircraft_engine_type_id" int,
  "registrant_type_id" int,
  "name" varchar,
  "address1" varchar,
  "address2" varchar,
  "city" varchar,
  "state" varchar,
  "zip" varchar,
  "region" varchar,
  "county" varchar,
  "country" varchar,
  "certification" varchar,
  "status_code" varchar,
  "mode_s_code" varchar,
  "fract_owner" varchar,
  "last_action_date" date,
  "cert_issue_date" date,
  "air_worth_date" date
) as copy from '/data/faa/aircraft.parquet' parquet;

alter table aircraft add constraint pk_aircraft primary key (tail_num);
alter table aircraft add constraint fk_aircraft_aircraft_models foreign key (aircraft_model_code) references aircraft_models(aircraft_model_code);

-----------------------------------------------------------------------------------------------------------------------------------

-- SELECT INFER_TABLE_DDL(
--          '/data/faa/flights.parquet'
--            USING PARAMETERS format = 'parquet', table_name = 'flights', table_type = 'external'
--          );

create external table "flights"(
  "carrier" varchar,
  "origin" varchar,
  "destination" varchar,
  "flight_num" varchar,
  "flight_time" int,
  "tail_num" varchar,
  "dep_time" timestamp,
  "arr_time" timestamp,
  "dep_delay" int,
  "arr_delay" int,
  "taxi_out" int,
  "taxi_in" int,
  "distance" int,
  "cancelled" varchar,
  "diverted" varchar,
  "id2" int
) as copy from '/data/faa/flights.parquet' parquet;

alter table flights add constraint pk_flights primary key (id2);
alter table flights add constraint fk_flights_carriers foreign key (carrier) references carriers(code);
alter table flights add constraint fk_flights_airports foreign key (origin) references airports(code);
alter table flights add constraint fk_flights_aircraft foreign key (tail_num) references aircraft(tail_num);
