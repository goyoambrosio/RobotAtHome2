select distinct
	raw.id,
	raw.time_stamp,
	homes.name as home_name,	
	rooms.name as room_name,
	home_sessions.name as home_session_name,
	raw.home_subsession_id,
	sensors.name as sensor_name
from
	raw, homes, rooms, home_sessions, sensors
where   homes.id = raw.home_id
	and rooms.id = raw.room_id
	and home_sessions.id = raw.home_session_id
	and sensors.id = raw.sensor_id