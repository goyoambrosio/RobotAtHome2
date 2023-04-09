-- Create an auxiliary table called sensor_observations_files table to store
-- new file names for intensity, depth and labels files.
-- The purpose is to gather all the files under the same folder to make the new
-- dataset version independent from the old one.
-- n_scan.txt files are not considered because their data is stored in [raw|lsrscan]_scans tables.

BEGIN TRANSACTION;

drop table if exists rh2_sensor_observations_files;
create table rh2_sensor_observations_files as
select
  rh2_sensor_observations.id,
	sensor_file_1,
	sensor_file_2,
	sensor_file_3,
	rh_homes.name home_name,
	substr(rh_rooms.name,instr(rh_rooms.name,"_")+1) room_name,
	rh2_sensor_observations.home_session_id home_session,
	rh2_sensor_observations.home_subsession_id home_subsession
from rh2_sensor_observations
inner join rh_homes on rh_homes.id=rh2_sensor_observations.home_id
inner join rh_rooms on rh_rooms.id=rh2_sensor_observations.room_id
where instr(sensor_file_1,"scan") == 0;

-- The new names are new_id + [intensity|depth|labels] + extension
update rh2_sensor_observations_files
set sensor_file_1 = id || substr(sensor_file_1,instr(sensor_file_1,"_"))
where sensor_file_1 <> "";

update rh2_sensor_observations_files
set sensor_file_2 = id || substr(sensor_file_2,instr(sensor_file_2,"_"))
where sensor_file_2 <> "";

update rh2_sensor_observations_files
set sensor_file_3 = id || substr(sensor_file_3,instr(sensor_file_3,"_"))
where sensor_file_3 <> "";

-- This table helps to rename and relocates files through a python script
drop table if exists rh2_old2new_rgbd_files;
create table rh2_old2new_rgbd_files as
select 
    rh2_sensor_observations.id id,
	  rh2_sensor_observations.files_path old_path,
    rh2_sensor_observations.sensor_file_1 old_file_1,
    rh2_sensor_observations.sensor_file_2 old_file_2,
    rh2_sensor_observations.sensor_file_3 old_file_3,
	"session_"|| (rh2_sensor_observations_files.home_session + 1) || "/" ||
	    rh2_sensor_observations_files.home_name || "/" ||
	    rh2_sensor_observations_files.room_name || "/" ||
	    "subsession_" || (rh2_sensor_observations_files.home_subsession + 1)  new_path,
    rh2_sensor_observations_files.sensor_file_1 new_file_1,
    rh2_sensor_observations_files.sensor_file_2 new_file_2,
    rh2_sensor_observations_files.sensor_file_3 new_file_3
from
    rh2_sensor_observations
inner join rh2_sensor_observations_files on rh2_sensor_observations.id = rh2_sensor_observations_files.id;

-- Indexes for rh2_old2new_rgbd_files
DROP INDEX IF EXISTS idx_rgbd_file_1;
CREATE INDEX idx_rgbd_file_1 ON rh2_old2new_rgbd_files (new_file_1);
DROP INDEX IF EXISTS idx_rgbd_file2;
CREATE INDEX idx_rgbd_file_2 ON rh2_old2new_rgbd_files (new_file_2);
DROP INDEX IF EXISTS idx_rgbd_file3;
CREATE INDEX idx_rgbd_file_3 ON rh2_old2new_rgbd_files (new_file_3);

drop table if exists rh2_sensor_observations_files;

COMMIT;


