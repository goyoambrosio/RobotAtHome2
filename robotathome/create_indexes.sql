BEGIN TRANSACTION;

-- Indexes for rh2_old2new_rgbd_files
DROP INDEX IF EXISTS idx_rgbd_file_1;
CREATE INDEX idx_rgbd_file_1 ON rh2_old2new_rgbd_files (new_file_1);
DROP INDEX IF EXISTS idx_rgbd_file2;
CREATE INDEX idx_rgbd_file_2 ON rh2_old2new_rgbd_files (new_file_2);
DROP INDEX IF EXISTS idx_rgbd_file3;
CREATE INDEX idx_rgbd_file_3 ON rh2_old2new_rgbd_files (new_file_3);

-- Indexes for rh2_old2new_scene_files
DROP INDEX IF EXISTS idx_scene_file;
CREATE INDEX idx_scene_file ON rh2_old2new_scene_files (new_file);

-- Indexes for rh_home_sessions
DROP INDEX IF EXISTS idx_home_session_name;
CREATE INDEX idx_home_session_name ON rh_home_sessions(name);

-- Indexes for rh_homes
DROP INDEX IF EXISTS idx_home_name;
CREATE INDEX idx_home_name ON rh_homes(name);

-- Indexes for rh_hometopo
DROP INDEX IF EXISTS idx_hometopo_home_id;
CREATE INDEX idx_hometopo_home_id ON rh_hometopo(home_id);
DROP INDEX IF EXISTS idx_hometopo_room1_id;
CREATE INDEX idx_hometopo_room1_id ON rh_hometopo(room1_id);
DROP INDEX IF EXISTS idx_hometopo_room2_id;
CREATE INDEX idx_hometopo_room2_id ON rh_hometopo(room2_id);

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

-- Indexes for rh_raw_scans
DROP INDEX IF EXISTS idx_raw_scans_sensor_observation_id;
CREATE INDEX idx_raw_scans_sensor_observation_id ON rh_raw_scans(sensor_observation_id);

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

-- Indexes for rh_lsrscan_scans
DROP INDEX IF EXISTS idx_lsrscan_scans_sensor_observation_id;
CREATE INDEX idx_lsrscan_scans_sensor_observation_id ON rh_lsrscan_scans(sensor_observation_id);

-- Indexes for rh_lblrgbd_labels
DROP INDEX IF EXISTS idx_lblrgbd_object_type_id;
CREATE INDEX idx_lblrgbd_object_type_id ON rh_lblrgbd_labels(object_type_id)

-- Indexes for rh_lblscene
DROP INDEX IF EXISTS idx_lblscene_home_session_id;
CREATE INDEX idx_lblscene_home_session_id ON rh_lblscene(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_lblscene_room_id;
CREATE INDEX idx_lblscene_room_id ON rh_lblscene(room_id);
DROP INDEX IF EXISTS idx_lblscene_home_id;
CREATE INDEX idx_lblscene_home_id ON rh_lblscene(home_id);

-- Indexes for rh_lblscene bboxes
DROP INDEX IF EXISTS idx_lblscene_bboxes_scene_id;
CREATE INDEX idx_lblscene_bboxes_scene_id ON rh_lblscene_bboxes(scene_id);
DROP INDEX IF EXISTS idx_lblscene_bboxes_object_id;
CREATE INDEX idx_lblscene_bboxes_object_id ON rh_lblscene_bboxes(object_id);

-- Indexes for rh_object_types
DROP INDEX IF EXISTS idx_object_types_name;
CREATE INDEX idx_object_types_name ON rh_object_types(name);

-- Indexes for rh_objects
DROP INDEX IF EXISTS idx_objects_name;
CREATE INDEX idx_objects_name ON rh_objects(name);
DROP INDEX IF EXISTS idx_objects_home_session_id;
CREATE INDEX idx_objects_home_session_id ON rh_objects(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_objects_room_id;
CREATE INDEX idx_objects_room_id ON rh_objects(room_id);
DROP INDEX IF EXISTS idx_objects_home_id;
CREATE INDEX idx_objects_home_id ON rh_objects(home_id);

-- Indexes for rh_objects_in_observation
DROP INDEX IF EXISTS idx_objects_in_observation_observation_id;
CREATE INDEX idx_objects_in_observation_observation_id ON rh_objects_in_observation(observation_id);
DROP INDEX IF EXISTS idx_objects_in_observation_object_id;
CREATE INDEX idx_objects_in_observation_object_id ON rh_objects_in_observation(object_id);

-- Indexes for rh_observations
DROP INDEX IF EXISTS idx_observations_home_session_id;
CREATE INDEX idx_observations_home_session_id ON rh_observations(home_session_id, home_subsession_id, room_id, sensor_id);
DROP INDEX IF EXISTS idx_observations_room_id;
CREATE INDEX idx_observations_room_id ON rh_observations(room_id);
DROP INDEX IF EXISTS idx_observations_home_id;
CREATE INDEX idx_observations_home_id ON rh_observations(home_id);

-- Indexes for rh_rctrscene
DROP INDEX IF EXISTS idx_rctrscene_home_session_id;
CREATE INDEX idx_rctrscene_home_session_id ON rh_rctrscene(home_session_id, home_subsession_id, room_id);
DROP INDEX IF EXISTS idx_rctrscene_room_id;
CREATE INDEX idx_rctrscene_room_id ON rh_rctrscene(room_id);
DROP INDEX IF EXISTS idx_rctrscene_home_id;
CREATE INDEX idx_rctrscene_home_id ON rh_rctrscene(home_id);

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

-- Indexes for rh_room_types
DROP INDEX IF EXISTS idx_room_types_name;
CREATE INDEX idx_room_types_name ON rh_room_types(name);

-- Indexes for rh_rooms
DROP INDEX IF EXISTS idx_rooms_name;
CREATE INDEX idx_rooms_name ON rh_rooms(name);
DROP INDEX IF EXISTS idx_rooms_room_type_id;
CREATE INDEX idx_rooms_room_type_id ON rh_rooms(room_type_id);
DROP INDEX IF EXISTS idx_rooms_home_id;
CREATE INDEX idx_rooms_home_id ON rh_rooms(home_id);

-- Indexes for rh_sensor_types
DROP INDEX IF EXISTS idx_sensor_types_name;
CREATE INDEX idx_sensor_types_name ON rh_sensor_types(name);

-- Indexes for rh_sensors
DROP INDEX IF EXISTS idx_sensors_name;
CREATE INDEX idx_sensors_name ON rh_sensors(name);
DROP INDEX IF EXISTS idx_sensors_sensor_type_id;
CREATE INDEX idx_sensors_sensor_type_id ON rh_sensors(sensor_type_id);

-- Indexes for rh_twodgeomap
DROP INDEX IF EXISTS idx_twodgeomap_room_id;
CREATE INDEX idx_twodgeomap_room_id ON rh_twodgeomap(room_id);
DROP INDEX IF EXISTS idx_twodgeomap_home_id;
CREATE INDEX idx_twodgeomap_home_id ON rh_twodgeomap(home_id);

COMMIT;
