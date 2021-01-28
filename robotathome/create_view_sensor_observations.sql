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
-- In this table 

-- Create a view with rows from raw table not in lblrgbd table
-- i.e., lblrgbd is a raw subset with labelled observations
drop view if exists raw_not_in_lblrgbd;
create view raw_not_in_lblrgbd as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from raw where sensor_id <> 0
except
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from lblrgbd;

-- Create a view with rows from raw table not in lsrscan table
-- i.e., lsrscan is a raw subset plus 
drop view if exists raw_not_in_lsrscan;
create view raw_not_in_lsrscan as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from raw where sensor_id = 0
except 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from lsrscan;

-- Create a view with raw rows not in lblrgbd table (36518 rgbd rows) nor lsrscan table (7600 lser scan rows)
-- plus lblrgbd (32937 rgbd rows)(ids begin in 100000)
-- plus lsrscan (39363 laser scan rows)(ids begin in 200000)
--   note: from the 39363 laser scan rows: 10635 intersect with raw table and 28728 don't intersect

drop view if exists sensor_observations;
create view sensor_observations as
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