BEGIN TRANSACTION;

------------------------------------------------------
--                 RH_RAW_SCANS                     --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_raw_scans`;
CREATE TABLE IF NOT EXISTS `rh_raw_scans` (
	`id`	integer NOT NULL UNIQUE,
	`shot_id`	integer,
	`scan`	real,
	`valid_scan`	integer,
	`sensor_observation_id`	integer,
	PRIMARY KEY(`id`)
  FOREIGN KEY(`sensor_observation_id`) REFERENCES `rh_raw`(`id`)
);

-- Indexes for rh_raw_scans
DROP INDEX IF EXISTS idx_raw_scans_sensor_observation_id;
CREATE INDEX idx_raw_scans_sensor_observation_id ON rh_raw_scans(sensor_observation_id);

------------------------------------------------------
--                   RH_RAW                         --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_raw`;
CREATE TABLE IF NOT EXISTS `rh_raw` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`home_id`	integer,
	`name`	text,
	`sensor_id`	integer,
	`sensor_pose_x`	real,
	`sensor_pose_y`	real,
	`sensor_pose_z`	real,
	`sensor_pose_yaw`	real,
	`sensor_pose_pitch`	real,
	`sensor_pose_roll`	real,
	`laser_aperture`	real,
	`laser_max_range`	real,
	`laser_num_of_scans`	integer,
	`time_stamp`	integer,
	`sensor_type`	integer,
	`sensor_file_1`	text,
	`sensor_file_2`	text,
	`sensor_file_3`	text,
	`files_path`	text,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`sensor_id`) REFERENCES `rh_sensors`(`id`),
  FOREIGN KEY(`sensor_type`) REFERENCES `rh_sensor_types`(`id`)
);

-- Indexes for rh_raw
DROP INDEX IF EXISTS idx_raw_time_stamp;
CREATE INDEX idx_raw_time_stamp ON rh_raw(time_stamp);
DROP INDEX IF EXISTS idx_raw_home_session_id;
CREATE INDEX idx_raw_home_session_id ON rh_raw(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_raw_room_id;
CREATE INDEX idx_raw_room_id ON rh_raw(room_id);
DROP INDEX IF EXISTS idx_raw_sensor_id;
CREATE INDEX idx_raw_sensor_id ON rh_raw(sensor_id);
DROP INDEX IF EXISTS idx_raw_home_id;
CREATE INDEX idx_raw_home_id ON rh_raw(home_id);

COMMIT;
