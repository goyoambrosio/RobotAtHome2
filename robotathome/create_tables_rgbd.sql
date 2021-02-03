BEGIN TRANSACTION;

------------------------------------------------------
--                   RH_RGBD                        --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_rgbd`;
CREATE TABLE IF NOT EXISTS `rh_rgbd` (
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
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`sensor_type`) REFERENCES `rh_sensor_types`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	PRIMARY KEY(`id`)
);

-- Indexes for rh_rgbd
DROP INDEX IF EXISTS idx_rgbd_time_stamp;
CREATE INDEX idx_rgbd_time_stamp ON rh_rgbd(time_stamp);
DROP INDEX IF EXISTS idx_rgbd_home_session_id;
CREATE INDEX idx_rgbd_home_session_id ON rh_rgbd(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_rgbd_room_id;
CREATE INDEX idx_rgbd_room_id ON rh_rgbd(room_id);
DROP INDEX IF EXISTS idx_rgbd_sensor_id;
CREATE INDEX idx_rgbd_sensor_id ON rh_rgbd(sensor_id);
DROP INDEX IF EXISTS idx_rgbd_home_id;
CREATE INDEX idx_rgbd_home_id ON rh_rgbd(home_id);

COMMIT;
