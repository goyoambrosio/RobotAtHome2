BEGIN TRANSACTION;


DROP TABLE IF EXISTS `rh2_old2new_scene_files`;
CREATE TABLE IF NOT EXISTS `rh2_old2new_scene_files` (
	`id`	INT NOT NULL UNIQUE,
	`old_file`	TEXT,
	`new_path`	TEXT,
	`new_file`	TEXT,
	PRIMARY KEY(`id`)
);
DROP TABLE IF EXISTS `rh2_old2new_rgbd_files`;
CREATE TABLE IF NOT EXISTS `rh2_old2new_rgbd_files` (
	`id`	INT NOT NULL UNIQUE,
	`old_path`	TEXT,
	`old_file_1`	TEXT,
	`old_file_2`	TEXT,
	`old_file_3`	TEXT,
	`new_path`	TEXT,
	`new_file_1`	TEXT,
	`new_file_2`	TEXT,
	`new_file_3`	TEXT,
	PRIMARY KEY(`id`)
);
DROP INDEX IF EXISTS `idx_twodgeomap_room_id`;
CREATE INDEX IF NOT EXISTS `idx_twodgeomap_room_id` ON `rh_twodgeomap` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_twodgeomap_home_id`;
CREATE INDEX IF NOT EXISTS `idx_twodgeomap_home_id` ON `rh_twodgeomap` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_sensors_sensor_type_id`;
CREATE INDEX IF NOT EXISTS `idx_sensors_sensor_type_id` ON `rh_sensors` (
	`sensor_type_id`
);
DROP INDEX IF EXISTS `idx_sensors_name`;
CREATE INDEX IF NOT EXISTS `idx_sensors_name` ON `rh_sensors` (
	`name`
);
DROP INDEX IF EXISTS `idx_sensor_types_name`;
CREATE INDEX IF NOT EXISTS `idx_sensor_types_name` ON `rh_sensor_types` (
	`name`
);
DROP INDEX IF EXISTS `idx_scene_file`;
CREATE INDEX IF NOT EXISTS `idx_scene_file` ON `rh2_old2new_scene_files` (
	`new_file`
);
DROP INDEX IF EXISTS `idx_rooms_room_type_id`;
CREATE INDEX IF NOT EXISTS `idx_rooms_room_type_id` ON `rh_rooms` (
	`room_type_id`
);
DROP INDEX IF EXISTS `idx_rooms_name`;
CREATE INDEX IF NOT EXISTS `idx_rooms_name` ON `rh_rooms` (
	`name`
);
DROP INDEX IF EXISTS `idx_rooms_home_id`;
CREATE INDEX IF NOT EXISTS `idx_rooms_home_id` ON `rh_rooms` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_room_types_name`;
CREATE INDEX IF NOT EXISTS `idx_room_types_name` ON `rh_room_types` (
	`name`
);
DROP INDEX IF EXISTS `idx_rgbd_time_stamp`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_time_stamp` ON `rh_rgbd` (
	`time_stamp`
);
DROP INDEX IF EXISTS `idx_rgbd_sensor_id`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_sensor_id` ON `rh_rgbd` (
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_rgbd_room_id`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_room_id` ON `rh_rgbd` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_rgbd_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_home_session_id` ON `rh_rgbd` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`,
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_rgbd_home_id`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_home_id` ON `rh_rgbd` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_rgbd_file_3`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_file_3` ON `rh2_old2new_rgbd_files` (
	`new_file_3`
);
DROP INDEX IF EXISTS `idx_rgbd_file_2`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_file_2` ON `rh2_old2new_rgbd_files` (
	`new_file_2`
);
DROP INDEX IF EXISTS `idx_rgbd_file_1`;
CREATE INDEX IF NOT EXISTS `idx_rgbd_file_1` ON `rh2_old2new_rgbd_files` (
	`new_file_1`
);
DROP INDEX IF EXISTS `idx_relations_room_id`;
CREATE INDEX IF NOT EXISTS `idx_relations_room_id` ON `rh_relations` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_relations_obj2_id_obj1_id`;
CREATE INDEX IF NOT EXISTS `idx_relations_obj2_id_obj1_id` ON `rh_relations` (
	`obj2_id`,
	`obj1_id`
);
DROP INDEX IF EXISTS `idx_relations_obj1_id_obj2_id`;
CREATE INDEX IF NOT EXISTS `idx_relations_obj1_id_obj2_id` ON `rh_relations` (
	`obj1_id`,
	`obj2_id`
);
DROP INDEX IF EXISTS `idx_relations_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_relations_home_session_id` ON `rh_relations` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`
);
DROP INDEX IF EXISTS `idx_relations_home_id`;
CREATE INDEX IF NOT EXISTS `idx_relations_home_id` ON `rh_relations` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_rctrscene_room_id`;
CREATE INDEX IF NOT EXISTS `idx_rctrscene_room_id` ON `rh_rctrscene` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_rctrscene_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_rctrscene_home_session_id` ON `rh_rctrscene` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`
);
DROP INDEX IF EXISTS `idx_rctrscene_home_id`;
CREATE INDEX IF NOT EXISTS `idx_rctrscene_home_id` ON `rh_rctrscene` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_raw_time_stamp`;
CREATE INDEX IF NOT EXISTS `idx_raw_time_stamp` ON `rh_raw` (
	`time_stamp`
);
DROP INDEX IF EXISTS `idx_raw_sensor_id`;
CREATE INDEX IF NOT EXISTS `idx_raw_sensor_id` ON `rh_raw` (
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_raw_scans_sensor_observation_id`;
CREATE INDEX IF NOT EXISTS `idx_raw_scans_sensor_observation_id` ON `rh_raw_scans` (
	`sensor_observation_id`
);
DROP INDEX IF EXISTS `idx_raw_room_id`;
CREATE INDEX IF NOT EXISTS `idx_raw_room_id` ON `rh_raw` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_raw_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_raw_home_session_id` ON `rh_raw` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`,
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_raw_home_id`;
CREATE INDEX IF NOT EXISTS `idx_raw_home_id` ON `rh_raw` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_observations_room_id`;
CREATE INDEX IF NOT EXISTS `idx_observations_room_id` ON `rh_observations` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_observations_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_observations_home_session_id` ON `rh_observations` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`,
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_observations_home_id`;
CREATE INDEX IF NOT EXISTS `idx_observations_home_id` ON `rh_observations` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_objects_room_id`;
CREATE INDEX IF NOT EXISTS `idx_objects_room_id` ON `rh_objects` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_objects_name`;
CREATE INDEX IF NOT EXISTS `idx_objects_name` ON `rh_objects` (
	`name`
);
DROP INDEX IF EXISTS `idx_objects_in_observation_observation_id`;
CREATE INDEX IF NOT EXISTS `idx_objects_in_observation_observation_id` ON `rh_objects_in_observation` (
	`observation_id`
);
DROP INDEX IF EXISTS `idx_objects_in_observation_object_id`;
CREATE INDEX IF NOT EXISTS `idx_objects_in_observation_object_id` ON `rh_objects_in_observation` (
	`object_id`
);
DROP INDEX IF EXISTS `idx_objects_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_objects_home_session_id` ON `rh_objects` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`
);
DROP INDEX IF EXISTS `idx_objects_home_id`;
CREATE INDEX IF NOT EXISTS `idx_objects_home_id` ON `rh_objects` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_object_types_name`;
CREATE INDEX IF NOT EXISTS `idx_object_types_name` ON `rh_object_types` (
	`name`
);
DROP INDEX IF EXISTS `idx_lsrscan_time_stamp`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_time_stamp` ON `rh_lsrscan` (
	`time_stamp`
);
DROP INDEX IF EXISTS `idx_lsrscan_sensor_id`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_sensor_id` ON `rh_lsrscan` (
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_lsrscan_scans_sensor_observation_id`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_scans_sensor_observation_id` ON `rh_lsrscan_scans` (
	`sensor_observation_id`
);
DROP INDEX IF EXISTS `idx_lsrscan_room_id`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_room_id` ON `rh_lsrscan` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_lsrscan_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_home_session_id` ON `rh_lsrscan` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`,
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_lsrscan_home_id`;
CREATE INDEX IF NOT EXISTS `idx_lsrscan_home_id` ON `rh_lsrscan` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_lblscene_room_id`;
CREATE INDEX IF NOT EXISTS `idx_lblscene_room_id` ON `rh_lblscene` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_lblscene_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_lblscene_home_session_id` ON `rh_lblscene` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`
);
DROP INDEX IF EXISTS `idx_lblscene_home_id`;
CREATE INDEX IF NOT EXISTS `idx_lblscene_home_id` ON `rh_lblscene` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_lblscene_bboxes_scene_id`;
CREATE INDEX IF NOT EXISTS `idx_lblscene_bboxes_scene_id` ON `rh_lblscene_bboxes` (
	`scene_id`
);
DROP INDEX IF EXISTS `idx_lblscene_bboxes_object_id`;
CREATE INDEX IF NOT EXISTS `idx_lblscene_bboxes_object_id` ON `rh_lblscene_bboxes` (
	`object_id`
);
DROP INDEX IF EXISTS `idx_lblrgbd_time_stamp`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_time_stamp` ON `rh_lblrgbd` (
	`time_stamp`
);
DROP INDEX IF EXISTS `idx_lblrgbd_sensor_id`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_sensor_id` ON `rh_lblrgbd` (
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_lblrgbd_room_id`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_room_id` ON `rh_lblrgbd` (
	`room_id`
);
DROP INDEX IF EXISTS `idx_lblrgbd_object_type_id`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_object_type_id` ON `rh_lblrgbd_labels` (
	`object_type_id`
);
DROP INDEX IF EXISTS `idx_lblrgbd_home_session_id`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_home_session_id` ON `rh_lblrgbd` (
	`home_session_id`,
	`home_subsession_id`,
	`room_id`,
	`sensor_id`
);
DROP INDEX IF EXISTS `idx_lblrgbd_home_id`;
CREATE INDEX IF NOT EXISTS `idx_lblrgbd_home_id` ON `rh_lblrgbd` (
	`home_id`
);
DROP INDEX IF EXISTS `idx_hometopo_room2_id`;
CREATE INDEX IF NOT EXISTS `idx_hometopo_room2_id` ON `rh_hometopo` (
	`room2_id`
);
DROP INDEX IF EXISTS `idx_hometopo_room1_id`;
CREATE INDEX IF NOT EXISTS `idx_hometopo_room1_id` ON `rh_hometopo` (
	`room1_id`
);
DROP INDEX IF EXISTS `idx_hometopo_home_id`;
CREATE INDEX IF NOT EXISTS `idx_hometopo_home_id` ON `rh_hometopo` (
	`home_id`
);
DROP VIEW IF EXISTS `rh2_sensor_observations`;
CREATE VIEW rh2_sensor_observations as
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
DROP VIEW IF EXISTS `rh2_scene_bb_objects`;
CREATE VIEW rh2_scene_bb_objects as 
select * from rh_lblscene_bboxes 
inner join rh_objects on rh_lblscene_bboxes.object_id=rh_objects.id;
DROP VIEW IF EXISTS `rh2_raw_not_in_lsrscan`;
CREATE VIEW rh2_raw_not_in_lsrscan as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_raw where sensor_id = 0
except 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_lsrscan;
DROP VIEW IF EXISTS `rh2_raw_not_in_lblrgbd`;
CREATE VIEW rh2_raw_not_in_lblrgbd as 
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_raw where sensor_id <> 0
except
select   time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id from rh_lblrgbd;
COMMIT;
