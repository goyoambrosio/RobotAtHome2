select 
    home_session_id, rh_home_sessions.name, 
	rh2_sensor_observations.home_id, rh_homes.name, 
	rh2_sensor_observations.room_id, rh_rooms.name, 
	rh2_sensor_observations.home_subsession_id, 
	rh2_sensor_observations.sensor_id, rh_sensors.name, 
	count(rh2_sensor_observations.id) as counter
from rh2_sensor_observations
inner join rh_home_sessions on home_session_id = rh_home_sessions.id
inner join rh_homes on rh2_sensor_observations.home_id = rh_homes.id
inner join rh_rooms on rh2_sensor_observations.room_id = rh_rooms.id
inner join rh_sensors on rh2_sensor_observations.sensor_id = rh_sensors.id
-- where --examples
--  rh2_sensor_observations.home_id = 2 and 
--	rh2_sensor_observations.home_subsession_id = 0 and 
--	rh2_sensor_observations.sensor_id > 0
group by 
    home_session_id, 
	rh2_sensor_observations.home_id, 
	rh2_sensor_observations.room_id, 
	rh2_sensor_observations.home_subsession_id, 
	rh2_sensor_observations.sensor_id

