-- USEFUL EXAMPLES

-- copy a table to another table
INSERT INTO Destination SELECT * FROM Source;

-- correlated subquery
SELECT *
FROM Table1
WHERE EXISTS (SELECT 1
              FROM Table2
              WHERE Table1.Value BETWEEN Table2.StartValue AND Table2.EndValue);
			  
-- get the first time_stamp			  
select min(time_stamp) from raw

-- add column
alter table aux_raw add column labelled integer not null default 0;

-- update a table from another table
update sensor_observations
set (sensor_file_1,
     sensor_file_2,
	 sensor_file_3) = (select old2new_rgbd_files.new_file_1,
	                          old2new_rgbd_files.new_file_2,
							  old2new_rgbd_files.new_file_3)
where exists (select * from old2new_rgbd_files
              where sensor_observations.id = old2new_rgbd_files.id);