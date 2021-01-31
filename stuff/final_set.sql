-- raw not in lblrgbd + lblrgbd
select 
raw.*
FROM raw, raw_not_in_lblrgbd
where raw.time_stamp = raw_not_in_lblrgbd.time_stamp
and raw.home_id = raw_not_in_lblrgbd.home_id
and raw.home_session_id = raw_not_in_lblrgbd.home_session_id
and raw.home_subsession_id = raw_not_in_lblrgbd.home_subsession_id
and raw.room_id = raw_not_in_lblrgbd.room_id
and raw.sensor_id = raw_not_in_lblrgbd.sensor_id

union

select 
raw.*
FROM raw, raw_not_in_lsrscan
where raw.time_stamp = raw_not_in_lsrscan.time_stamp
and raw.home_id = raw_not_in_lsrscan.home_id
and raw.home_session_id = raw_not_in_lsrscan.home_session_id
and raw.home_subsession_id = raw_not_in_lsrscan.home_subsession_id
and raw.room_id = raw_not_in_lsrscan.room_id
and raw.sensor_id = raw_not_in_lsrscan.sensor_id

union

select * from lblrgbd

union 

select * from lsrscan