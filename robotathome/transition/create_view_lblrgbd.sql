begin transaction;
drop view if exists rh2_lblrgbd;
create view rh2_lblrgbd as 
select 
    rh_lblrgbd.id,
	rh_lblrgbd.home_session_id as hs_id,
    rh_home_sessions.name as hs_name,
	rh_lblrgbd.home_subsession_id as hss_id,
	rh_lblrgbd.home_id as h_id,
    rh_homes.name as h_name,
	rh_lblrgbd.room_id as r_id,
    rh_rooms.name as r_name,
	rh_lblrgbd.sensor_id as s_id,
	rh_sensors.name as s_name,
	rh_lblrgbd.time_stamp as t,
	rh_lblrgbd.sensor_pose_x as s_px,
	rh_lblrgbd.sensor_pose_y as s_py,
	rh_lblrgbd.sensor_pose_z as s_pz,
	rh_lblrgbd.sensor_pose_yaw as s_pya,
	rh_lblrgbd.sensor_pose_pitch as s_ppi,
	rh_lblrgbd.sensor_pose_roll as s_pro,
	rh2_old2new_rgbd_files.new_file_1 as f1,
	rh2_old2new_rgbd_files.new_file_2 as f2,
	rh2_old2new_rgbd_files.new_file_3 as f3,
	rh2_old2new_rgbd_files.new_path as pth
from rh_lblrgbd
inner join rh_home_sessions on home_session_id = rh_home_sessions.id
inner join rh_homes on rh_lblrgbd.home_id = rh_homes.id
inner join rh_rooms on rh_lblrgbd.room_id = rh_rooms.id
inner join rh_sensors on rh_lblrgbd.sensor_id = rh_sensors.id
inner join rh2_old2new_rgbd_files on rh2_old2new_rgbd_files.id = rh_lblrgbd.id
--order by
--	rh_lblrgbd.time_stamp asc
commit;


