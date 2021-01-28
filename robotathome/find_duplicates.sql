-- Find duplicate registers
select time_stamp, home_session_id, home_subsession_id, room_id, sensor_id
from lblrgbd
group by time_stamp, home_session_id, home_subsession_id, room_id, sensor_id
having count(time_stamp + home_session_id + home_subsession_id + home_id + room_id + sensor_id) > 1;