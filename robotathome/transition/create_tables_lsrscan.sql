BEGIN TRANSACTION;

------------------------------------------------------
--                RH_LSRSCAN_SCANS                  --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lsrscan_scans`;
CREATE TABLE IF NOT EXISTS `rh_lsrscan_scans` (
	`id`	integer NOT NULL UNIQUE,
	`shot_id`	integer,
	`scan`	real,
	`valid_scan`	integer,
	`sensor_observation_id`	integer,
	PRIMARY KEY(`id`),
  FOREIGN KEY(`sensor_observation_id`) REFERENCES `rh_lsrscan`(`id`)
);

-- Indexes for rh_lsrscan_scans
DROP INDEX IF EXISTS idx_lsrscan_scans_sensor_observation_id;
CREATE INDEX idx_lsrscan_scans_sensor_observation_id ON rh_lsrscan_scans(sensor_observation_id);

------------------------------------------------------
--                  RH_LSRSCAN                      --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lsrscan`;
CREATE TABLE IF NOT EXISTS `rh_lsrscan` (
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
	FOREIGN KEY(`sensor_type`) REFERENCES `rh_sensor_types`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`sensor_id`) REFERENCES `rh_sensors`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`)
);

-- Indexes for rh_lsrscan
DROP INDEX IF EXISTS idx_lsrscan_time_stamp;
CREATE INDEX idx_lsrscan_time_stamp ON rh_lsrscan(time_stamp);
DROP INDEX IF EXISTS idx_lsrscan_home_session_id;
CREATE INDEX idx_lsrscan_home_session_id ON rh_lsrscan(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_lsrscan_room_id;
CREATE INDEX idx_lsrscan_room_id ON rh_lsrscan(room_id);
DROP INDEX IF EXISTS idx_lsrscan_sensor_id;
CREATE INDEX idx_lsrscan_sensor_id ON rh_lsrscan(sensor_id);
DROP INDEX IF EXISTS idx_lsrscan_home_id;
CREATE INDEX idx_lsrscan_home_id ON rh_lsrscan(home_id);


COMMIT;
