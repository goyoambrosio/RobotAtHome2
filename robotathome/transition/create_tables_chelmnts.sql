BEGIN TRANSACTION;

------------------------------------------------------
--                 RH_OBJECTS                       --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_objects`;
CREATE TABLE IF NOT EXISTS `rh_objects` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`name`	text,
	`object_type_id`	integer,
	`planarity`	real,
	`scatter`	real,
	`linearity`	real,
	`min_height`	real,
	`max_height`	real,
	`centroid_x`	real,
	`centroid_y`	real,
	`centroid_z`	real,
	`volume`	real,
	`biggest_area`	real,
	`orientation`	real,
	`hue_mean`	real,
	`saturation_mean`	real,
	`value_mean`	real,
	`hue_stdv`	real,
	`saturation_stdv`	real,
	`value_stdv`	real,
	`hue_histogram_0`	real,
	`hue_histogram_1`	real,
	`hue_histogram_2`	real,
	`hue_histogram_3`	real,
	`hue_histogram_4`	real,
	`value_histogram_0`	real,
	`value_histogram_1`	real,
	`value_histogram_2`	real,
	`value_histogram_3`	real,
	`value_histogram_4`	real,
	`saturation_histogram_0`	real,
	`saturation_histogram_1`	real,
	`saturation_histogram_2`	real,
	`saturation_histogram_3`	real,
	`saturation_histogram_4`	real,
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`object_type_id`) REFERENCES `rh_object_types`(`id`)
);

-- Indexes for rh_objects
DROP INDEX IF EXISTS idx_objects_name;
CREATE INDEX idx_objects_name ON rh_objects(name);
DROP INDEX IF EXISTS idx_objects_home_session_id;
CREATE INDEX idx_objects_home_session_id ON rh_objects(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_objects_room_id;
CREATE INDEX idx_objects_room_id ON rh_objects(room_id);
DROP INDEX IF EXISTS idx_objects_home_id;
CREATE INDEX idx_objects_home_id ON rh_objects(home_id);

------------------------------------------------------
--                 RH_OBJECT_TYPES                  --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_object_types`;
CREATE TABLE IF NOT EXISTS `rh_object_types` (
	`id`	integer NOT NULL UNIQUE,
	`name`	text,
	PRIMARY KEY(`id`)
);

-- Indexes for rh_object_types
DROP INDEX IF EXISTS idx_object_types_name;
CREATE INDEX idx_object_types_name ON rh_object_types(name);

------------------------------------------------------
--                 RH_RELATIONS                     --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_relations`;
CREATE TABLE IF NOT EXISTS `rh_relations` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`obj1_id`	integer,
	`obj2_id`	integer,
	`minimum_distance`	real,
	`perpendicularity`	real,
	`vertical_distance`	real,
	`volume_ratio`	real,
	`is_on`	integer,
	`abs_hue_stdv_diff`	real,
	`abs_saturation_stdv_diff`	real,
	`abs_value_stdv_diff`	real,
	`abs_hue_mean_diff`	real,
	`abs_saturation_mean_diff`	real,
	`abs_value_mean_diff`	real,
	FOREIGN KEY(`obj1_id`) REFERENCES `rh_objects`(`id`),
	FOREIGN KEY(`obj2_id`) REFERENCES `rh_objects`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	PRIMARY KEY(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`)
);

-- Indexes for rh_relations
DROP INDEX IF EXISTS idx_relations_home_session_id;
CREATE INDEX idx_relations_home_session_id ON rh_relations(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_relations_room_id;
CREATE INDEX idx_relations_room_id ON rh_relations(room_id);
DROP INDEX IF EXISTS idx_relations_home_id;
CREATE INDEX idx_relations_home_id ON rh_relations(home_id);
DROP INDEX IF EXISTS idx_relations_obj1_id_obj2_id;
CREATE INDEX idx_relations_obj1_id_obj2_id ON rh_relations(obj1_id, obj2_id);
DROP INDEX IF EXISTS idx_relations_obj2_id_obj1_id;
CREATE INDEX idx_relations_obj2_id_obj1_id ON rh_relations(obj2_id, obj1_id);

------------------------------------------------------
--                 RH_OBSERVATIONS                  --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_observations`;
CREATE TABLE IF NOT EXISTS `rh_observations` (
	`id`	integer NOT NULL UNIQUE,
	`room_id`	integer,
	`home_id`	integer,
	`home_session_id`	integer,
	`home_subsession_id`	integer,
	`sensor_id`	integer,
	`mean_hue`	real,
	`mean_saturation`	real,
	`mean_value`	real,
	`hue_stdv`	real,
	`saturation_stdv`	real,
	`value_stdv`	real,
	`hue_histogram_1`	real,
	`hue_histogram_2`	real,
	`hue_histogram_3`	real,
	`hue_histogram_4`	real,
	`hue_histogram_5`	real,
	`saturation_histogram_1`	real,
	`saturation_histogram_2`	real,
	`saturation_histogram_3`	real,
	`saturation_histogram_4`	real,
	`saturation_histogram_5`	real,
	`value_histogram_1`	real,
	`value_histogram_2`	real,
	`value_histogram_3`	real,
	`value_histogram_4`	real,
	`value_histogram_5`	real,
	`distance`	real,
	`foot_print`	real,
	`volume`	real,
	`mean_mean_hue`	real,
	`mean_mean_saturation`	real,
	`mean_mean_value`	real,
	`mean_hue_stdv`	real,
	`mean_saturation_stdv`	real,
	`mean_value_stdv`	real,
	`mean_hue_histogram_1`	real,
	`mean_hue_histogram_2`	real,
	`mean_hue_histogram_3`	real,
	`mean_hue_histogram_4`	real,
	`mean_hue_histogram_5`	real,
	`mean_saturation_histogram_1`	real,
	`mean_saturation_histogram_2`	real,
	`mean_saturation_histogram_3`	real,
	`mean_saturation_histogram_4`	real,
	`mean_saturation_histogram_5`	real,
	`mean_value_histogram_1`	real,
	`mean_value_histogram_2`	real,
	`mean_value_histogram_3`	real,
	`mean_value_histogram_4`	real,
	`mean_value_histogram_5`	real,
	`mean_distance`	real,
	`mean_foot_print`	real,
	`mean_volume`	real,
	`scan_area`	real,
	`scan_elongation`	real,
	`scan_mean_distance`	real,
	`scan_distance_stdv`	real,
	`scan_num_of_points`	integer,
	`scan_compactness`	real,
	`scan_compactness2`	real,
	`scan_linearity`	real,
	`scan_scatter`	real,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	FOREIGN KEY(`home_session_id`) REFERENCES `rh_home_sessions`(`id`),
	FOREIGN KEY(`sensor_id`) REFERENCES `rh_sensors`(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`)
);

-- Indexes for rh_observations
DROP INDEX IF EXISTS idx_observations_home_session_id;
CREATE INDEX idx_observations_home_session_id ON rh_observations(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_observations_room_id;
CREATE INDEX idx_observations_room_id ON rh_observations(room_id);
DROP INDEX IF EXISTS idx_observations_home_id;
CREATE INDEX idx_observations_home_id ON rh_observations(home_id);

------------------------------------------------------
--             RH_OBJECTS_IN_OBSERVATION            --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_objects_in_observation`;
CREATE TABLE IF NOT EXISTS `rh_objects_in_observation` (
	`id`	integer NOT NULL UNIQUE,
	`observation_id`	integer,
	`object_id`	integer,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`observation_id`) REFERENCES `rh_observations`(`id`)
);

-- Indexes for rh_objects_in_observation
DROP INDEX IF EXISTS idx_objects_in_observation_observation_id;
CREATE INDEX idx_objects_in_observation_observation_id ON rh_objects_in_observation(observation_id);
DROP INDEX IF EXISTS idx_objects_in_observation_object_id;
CREATE INDEX idx_objects_in_observation_object_id ON rh_objects_in_observation(object_id);

COMMIT;
