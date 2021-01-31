-- Example of create view with joins

drop view if exists my_raw;

create view my_raw
as 
SELECT DISTINCT
	raw.id,
	raw.time_stamp-(select min(time_stamp) from raw),
	homes.name as home_name,	
	rooms.name as room_name,
	home_sessions.name as home_session_name,
	raw.home_subsession_id,
	sensors.name as sensor_name
from
	raw
inner join homes on homes.id = raw.home_id
inner join rooms on rooms.id = raw.room_id
inner join home_sessions on home_sessions.id = raw.home_session_id
inner join sensors on sensors.id = raw.sensor_id
order by raw.time_stamp

	