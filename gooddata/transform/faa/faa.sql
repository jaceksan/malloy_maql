alter table airports add name varchar
;

update airports set name = code || '-' || full_name
;
