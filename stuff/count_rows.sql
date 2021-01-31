-- count distinct rows

-- sensor_id <> 0 -> rgbd shots 
-- sensor_id = 0 -> laser shots 
select count(*) from raw;
select count (distinct time_stamp+home_session_id+home_subsession_id+home_id+room_id+sensor_id) from raw; --where sensor_id = 0 | where sensor_id <> 0

select count(*) from rgbd;
select count (distinct time_stamp+home_session_id+home_subsession_id+home_id+room_id+sensor_id) from rgbd;

select count(*) from lblrgbd;
select count (distinct time_stamp+home_session_id+home_subsession_id+home_id+room_id+sensor_id) from lblrgbd;

select count(*) from lsrscan;
select count (distinct time_stamp+home_session_id+home_subsession_id+home_id+room_id+sensor_id) from lsrscan;