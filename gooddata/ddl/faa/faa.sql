
;

-----------------------------------------------------------------------------------------------------------------------------------

;

-----------------------------------------------------------------------------------------------------------------------------------

create table "flights"(
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
  "id2" int,
  constraint "pk_flights" primary key ("id2"),
  constraint "fk_flights_carriers" foreign key ("carrier") references "carriers"("code"),
  constraint "fk_flights_airports" foreign key ("origin") references "airports"("code"),
  constraint "fk_flights_aircraft" foreign key ("tail_num") references "aircraft"("tail_num")
)
;
