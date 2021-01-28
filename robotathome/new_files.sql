drop table if exists sensor_observations_files;
create table sensor_observations_files as
select id, sensor_file_1, sensor_file_2, sensor_file_3
from sensor_observations