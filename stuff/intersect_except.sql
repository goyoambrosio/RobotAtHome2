-- lblrgbd is the labelled subset of rgbd, which is the rgb subset of raw
select  distinct time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from lsrscan
except
select  distinct time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from raw where sensor_id = 0;
