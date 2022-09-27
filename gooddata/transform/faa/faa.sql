alter table airports add name varchar
;

update airports set name = code || '-' || full_name
;

create or replace view airports_dest as select * from airports
;

create or replace view airports_origin as select * from airports
;
