BEGIN TRANSACTION;

------------------------------------------------------
--                  RH_RCTRSCENE                    --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_rctrscene`;
CREATE TABLE IF NOT EXISTS `rh_rctrscene` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`home_id`	integer,
	`scene_file`	text,
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`)
);

-- Indexes for rh_rctrscene
DROP INDEX IF EXISTS idx_rctrscene_home_session_id;
CREATE INDEX idx_rctrscene_home_session_id ON rh_rctrscene(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_rctrscene_room_id;
CREATE INDEX idx_rctrscene_room_id ON rh_rctrscene(room_id);
DROP INDEX IF EXISTS idx_rctrscene_home_id;
CREATE INDEX idx_rctrscene_home_id ON rh_rctrscene(home_id);


COMMIT;
