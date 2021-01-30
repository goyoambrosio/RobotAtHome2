-- Create an auxiliary table called sensor_observations_files table to store 
-- new file names for intensity, depth and labels files.
-- The purpose is to gather all the files under the same folder to make the new 
-- dataset version independent from the old one.
-- n_scan.txt files are not considered because their data is stored in [raw|lsrscan]_scans tables.

drop table if exists sensor_observations_files;
create table sensor_observations_files as
select id, sensor_file_1, sensor_file_2, sensor_file_3
from sensor_observations
where instr(sensor_file_1,"scan") == 0;

-- The new names are new_id + [intensity|depth|labels] + extension
update sensor_observations_files
set sensor_file_1 = id || substr(sensor_file_1,instr(sensor_file_1,"_"))
where sensor_file_1 <> "";

update sensor_observations_files
set sensor_file_2 = id || substr(sensor_file_2,instr(sensor_file_2,"_"))
where sensor_file_2 <> "";

update sensor_observations_files
set sensor_file_3 = id || substr(sensor_file_3,instr(sensor_file_3,"_"))
where sensor_file_3 <> "";

-- This table helps to rename and relocates files through a python script
drop table if exists old2new_rgbd_files;
create table old2new_rgbd_files as
select 
    sensor_observations.id id, 
    sensor_observations.sensor_file_1 old_file_1, 
    sensor_observations.sensor_file_2 old_file_2, 
    sensor_observations.sensor_file_3 old_file_3, 
    sensor_observations.files_path,
    sensor_observations_files.sensor_file_1 new_file_1,
    sensor_observations_files.sensor_file_2 new_file_2,
    sensor_observations_files.sensor_file_3 new_file_3
from 
    sensor_observations 
inner join sensor_observations_files on sensor_observations.id = sensor_observations_files.id;

drop table if exists sensor_observations_files;

update sensor_observations
set (sensor_file_1,
     sensor_file_2,
	 sensor_file_3) = (select old2new_rgbd_files.new_file_1,
	                          old2new_rgbd_files.new_file_2,
							  old2new_rgbd_files.new_file_3)
where exists (select * from old2new_rgbd_files
              where sensor_observations.id = old2new_rgbd_files.id);

 = old2new_rgbd_files.new_file_1
from old2new_rgbd_files
where sensor_observations.id = old2new_rgbd_files.id;

