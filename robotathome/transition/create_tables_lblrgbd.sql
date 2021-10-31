BEGIN TRANSACTION;

------------------------------------------------------
--                   RH_LBLRGBD                     --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lblrgbd`;
CREATE TABLE IF NOT EXISTS `rh_lblrgbd` (
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
	FOREIGN KEY(`sensor_id`) REFERENCES `rh_sensors`(`id`),
	FOREIGN KEY(`sensor_type`) REFERENCES `rh_sensor_types`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`)
);

-- Indexes for rh_lblrgbd
DROP INDEX IF EXISTS idx_lblrgbd_time_stamp;
CREATE INDEX idx_lblrgbd_time_stamp ON rh_lblrgbd(time_stamp);
DROP INDEX IF EXISTS idx_lblrgbd_home_session_id;
CREATE INDEX idx_lblrgbd_home_session_id ON rh_lblrgbd(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_lblrgbd_room_id;
CREATE INDEX idx_lblrgbd_room_id ON rh_lblrgbd(room_id);
DROP INDEX IF EXISTS idx_lblrgbd_sensor_id;
CREATE INDEX idx_lblrgbd_sensor_id ON rh_lblrgbd(sensor_id);
DROP INDEX IF EXISTS idx_lblrgbd_home_id;
CREATE INDEX idx_lblrgbd_home_id ON rh_lblrgbd(home_id);

------------------------------------------------------
--                   RH_LBLRGBD_LABELS              --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lblrgbd_labels`;
CREATE TABLE IF NOT EXISTS `rh_lblrgbd_labels` (
	`id`	integer NOT NULL UNIQUE,
	`local_id`	integer,
	`name`	text,
	`sensor_observation_id`	integer,
	`object_type_id`	integer,
	FOREIGN KEY(`object_type_id`) REFERENCES `rh_object_types`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`sensor_observation_id`) REFERENCES `rh_lblrgbd`(`id`)
);

-- Indexes for rh_lblrgbd_labels
DROP INDEX IF EXISTS idx_lblrgbd_labels_object_type_id;
CREATE INDEX idx_lblrgbd_labels_object_type_id ON rh_lblrgbd_labels(object_type_id);


COMMIT;
