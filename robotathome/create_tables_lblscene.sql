BEGIN TRANSACTION;

------------------------------------------------------
--                  RH_LBLSCENE                     --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lblscene`;
CREATE TABLE IF NOT EXISTS `rh_lblscene` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`home_id`	integer,
	`scene_file`	text,
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	PRIMARY KEY(`id`)
);

-- Indexes for rh_lblscene
DROP INDEX IF EXISTS idx_lblscene_home_session_id;
CREATE INDEX idx_lblscene_home_session_id ON rh_lblscene(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_lblscene_room_id;
CREATE INDEX idx_lblscene_room_id ON rh_lblscene(room_id);
DROP INDEX IF EXISTS idx_lblscene_home_id;
CREATE INDEX idx_lblscene_home_id ON rh_lblscene(home_id);

------------------------------------------------------
--                  RH_LBLSCENE_BBOXES              --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_lblscene_bboxes`;
CREATE TABLE `rh_lblscene_bboxes` (
	`id`	integer NOT NULL UNIQUE,
	`local_id`	integer,
	`scene_id`	integer,
	`object_id`	integer,
	`object_name`	text,
	`bb_pose_x`	real,
	`bb_pose_y`	real,
	`bb_pose_z`	real,
	`bb_pose_yaw`	real,
	`bb_pose_pitch`	real,
	`bb_pose_roll`	real,
	`bb_corner1_x`	real,
	`bb_corner1_y`	real,
	`bb_corner1_z`	real,
	`bb_corner2_x`	real,
	`bb_corner2_y`	real,
	`bb_corner2_z`	real,
	FOREIGN KEY(`object_id`) REFERENCES `rh_objects`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`scene_id`) REFERENCES `rh_lblscene`(`id`)
);

-- Indexes for rh_lblscene bboxes
DROP INDEX IF EXISTS idx_lblscene_bboxes_scene_id;
CREATE INDEX idx_lblscene_bboxes_scene_id ON rh_lblscene_bboxes(scene_id);
DROP INDEX IF EXISTS idx_lblscene_bboxes_object_id;
CREATE INDEX idx_lblscene_bboxes_object_id ON rh_lblscene_bboxes(object_id);


COMMIT;
