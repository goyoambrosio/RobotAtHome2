select 
    home_session_id, rh_home_sessions.name, 
	rh_lblrgbd.home_id, rh_homes.name, 
	rh_lblrgbd.room_id, rh_rooms.name, 
	rh_lblrgbd.home_subsession_id, 
	rh_lblrgbd.sensor_id, rh_sensors.name, 
	count(rh_lblrgbd.id) as counter
from rh_lblrgbd
inner join rh_home_sessions on home_session_id = rh_home_sessions.id
inner join rh_homes on rh_lblrgbd.home_id = rh_homes.id
inner join rh_rooms on rh_lblrgbd.room_id = rh_rooms.id
inner join rh_sensors on rh_lblrgbd.sensor_id = rh_sensors.id
-- where -- where examples
--    rh_homes.name = 'rx2'
--    rh_lblrgbd.home_id = 2 and 
--	  rh_lblrgbd.home_subsession_id = 0 and 
--	  rh_lblrgbd.sensor_id > 0
group by 
    home_session_id, 
	rh_lblrgbd.home_id, 
	rh_lblrgbd.room_id, 
	rh_lblrgbd.home_subsession_id, 
	rh_lblrgbd.sensor_id
order by
	rh_lblrgbd.time_stamp

