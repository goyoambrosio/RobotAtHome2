BEGIN TRANSACTION;

------------------------------------------------------
--                 RH_HOMES                         --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_homes`;
CREATE TABLE IF NOT EXISTS `rh_homes` (
	`id`	integer NOT NULL UNIQUE,
	`name`	text,
	PRIMARY KEY(`id`)
);

-- Indexes for rh_homes
DROP INDEX IF EXISTS idx_home_name;
CREATE INDEX idx_home_name ON rh_homes(name);

------------------------------------------------------
--                 RH_HOME_SESSIONS                 --
------------------------------------------------------

DROP TABLE IF EXISTS `rh_home_sessions`;
CREATE TABLE IF NOT EXISTS `rh_home_sessions` (
	`id`	integer NOT NULL UNIQUE,
	`home_id`	integer,
	`name`	text,
	PRIMARY KEY(`id`)
);

-- Indexes for rh_home_sessions
DROP INDEX IF EXISTS idx_home_session_name;
CREATE INDEX idx_home_session_name ON rh_home_sessions(name);

------------------------------------------------------
--                 RH_ROOMS                         --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_rooms`;
CREATE TABLE IF NOT EXISTS `rh_rooms` (
	`id`	integer NOT NULL UNIQUE,
	`home_id`	integer,
	`name`	text,
	`room_type_id`	integer,
	FOREIGN KEY(`room_type_id`) REFERENCES `rh_room_types`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	PRIMARY KEY(`id`)
);

-- Indexes for rh_rooms
DROP INDEX IF EXISTS idx_rooms_name;
CREATE INDEX idx_rooms_name ON rh_rooms(name);
DROP INDEX IF EXISTS idx_rooms_room_type_id;
CREATE INDEX idx_rooms_room_type_id ON rh_rooms(room_type_id);
DROP INDEX IF EXISTS idx_rooms_home_id;
CREATE INDEX idx_rooms_home_id ON rh_rooms(home_id);

------------------------------------------------------
--                 RH_ROOM_TYPES                    --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_room_types`;
CREATE TABLE IF NOT EXISTS `rh_room_types` (
	`id`	integer NOT NULL UNIQUE,
	`name`	text,
	PRIMARY KEY(`id`)
);

-- Indexes for rh_room_types
DROP INDEX IF EXISTS idx_room_types_name;
CREATE INDEX idx_room_types_name ON rh_room_types(name);

------------------------------------------------------
--                 RH_SENSORS                       --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_sensors`;
CREATE TABLE IF NOT EXISTS `rh_sensors` (
	`id`	integer NOT NULL UNIQUE,
	`sensor_type_id`	integer,
	`name`	text,
	FOREIGN KEY(`sensor_type_id`) REFERENCES `rh_sensor_types`(`id`),
	PRIMARY KEY(`id`)
);

-- Indexes for rh_sensors
DROP INDEX IF EXISTS idx_sensors_name;
CREATE INDEX idx_sensors_name ON rh_sensors(name);
DROP INDEX IF EXISTS idx_sensors_sensor_type_id;
CREATE INDEX idx_sensors_sensor_type_id ON rh_sensors(sensor_type_id);

------------------------------------------------------
--                 RH_SENSOR_TYPES                  --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_sensor_types`;
CREATE TABLE IF NOT EXISTS `rh_sensor_types` (
	`id`	integer NOT NULL UNIQUE,
	`name`	text,
	PRIMARY KEY(`id`)
);

-- Indexes for rh_sensor_types
DROP INDEX IF EXISTS idx_sensor_types_name;
CREATE INDEX idx_sensor_types_name ON rh_sensor_types(name);

COMMIT;
