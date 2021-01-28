-- Show duplicates

SELECT a.time_stamp, a.home_session_id, a.home_subsession_id, a.home_id, a.room_id, a.sensor_id
FROM raw a
JOIN (
select time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id
from raw 
group by time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id
having count(time_stamp+home_session_id+home_subsession_id+home_id+room_id+sensor_id) > 1
 ) b
ON a.home_session_id = b.home_session_id
AND a.home_subsession_id = b.home_subsession_id
AND a.room_id = b.room_id
AND a.home_id = b.home_id
AND a.sensor_id = b.sensor_id
AND a.time_stamp = b.time_stamp
ORDER BY a.home_session_id
