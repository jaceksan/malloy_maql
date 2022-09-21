set search_path to faa,public;

create or replace view airports_dest as select * from airports;
create or replace view airports_origin as select * from airports;
