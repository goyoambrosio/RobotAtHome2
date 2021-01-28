-- create aux_raw
drop table if exists aux_raw;
create table aux_raw as
	select * from raw;
	
drop index if exists idx_aux_raw;
create index idx_aux_raw on raw(time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id);