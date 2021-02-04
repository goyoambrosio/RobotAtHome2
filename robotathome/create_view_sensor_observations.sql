-- Create a view with all sensor observations sets, i.e. rejected-for-labelling raw rows plus
-- labelled rgbd rows plus laser scan rows.

-- raw table has 87690 rows: 69455 rgbd + 18235 laser scans observations
-- rgbd rows have two files: depth.png, intensity.png
-- laser scans have one file: scan.txt

-- rgbd table is a raw subset with only rgbd observations.distance.
-- Obviously it has 69455 rows

-- lblrgbd table is a rgbd table subset in which objects have been labelled.
-- It has 32937 rows with an added file: labels.txt

-- lsrscan is a table with 39363 rows composed by 10635 rows coming from 
-- the raw table, plus 28728 rows added by extra scanning sessions not 
-- included in the original raw table.

BEGIN TRANSACTION;

-- Create a view with rows from raw table not in lblrgbd table
-- i.e., lblrgbd is a raw subset with labelled observations
drop view if exists rh2_raw_not_in_lblrgbd;
create view rh2_raw_not_in_lblrgbd as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_raw where sensor_id <> 0
except
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_lblrgbd;

-- Create a view with rows from raw table not in lsrscan table
-- i.e., lsrscan is a raw subset plus 
drop view if exists rh2_raw_not_in_lsrscan;
create view rh2_raw_not_in_lsrscan as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_raw where sensor_id = 0
except 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_lsrscan;

-- Create a view with raw rows not in lblrgbd table (36518 rgbd rows) nor lsrscan table (7600 laser scan rows)
-- plus lblrgbd (32937 rgbd rows)(ids begin in 100000)
-- plus lsrscan (39363 laser scan rows)(ids begin in 200000)
--   note: from the 39363 laser scan rows: 10635 intersect with raw table and 28728 don't intersect

drop view if exists rh2_sensor_observations;
create view rh2_sensor_observations as
select 
rh_raw.*
FROM rh_raw, rh2_raw_not_in_lblrgbd
where rh_raw.time_stamp = rh2_raw_not_in_lblrgbd.time_stamp
and rh_raw.home_id = rh2_raw_not_in_lblrgbd.home_id
and rh_raw.home_session_id = rh2_raw_not_in_lblrgbd.home_session_id
and rh_raw.home_subsession_id = rh2_raw_not_in_lblrgbd.home_subsession_id
and rh_raw.room_id = rh2_raw_not_in_lblrgbd.room_id
and rh_raw.sensor_id = rh2_raw_not_in_lblrgbd.sensor_id

union

select 
rh_raw.*
FROM rh_raw, rh2_raw_not_in_lsrscan
where rh_raw.time_stamp = rh2_raw_not_in_lsrscan.time_stamp
and rh_raw.home_id = rh2_raw_not_in_lsrscan.home_id
and rh_raw.home_session_id = rh2_raw_not_in_lsrscan.home_session_id
and rh_raw.home_subsession_id = rh2_raw_not_in_lsrscan.home_subsession_id
and rh_raw.room_id = rh2_raw_not_in_lsrscan.room_id
and rh_raw.sensor_id = rh2_raw_not_in_lsrscan.sensor_id

union

select * from rh_lblrgbd

union 

select * from rh_lsrscan;

COMMIT;
