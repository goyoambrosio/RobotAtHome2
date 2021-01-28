-- Create indexes on raw and derivated tables

drop index if exists idx_raw;
create index idx_raw on raw(time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id);

drop index if exists idx_rgbd;
create index idx_rgbd on rgbd(time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id);

drop index if exists idx_lblrgbd;
create index idx_lblrgbd on lblrgbd(time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id);

drop index if exists idx_lsrscan;
create index idx_lsrscan on lsrscan(time_stamp, home_session_id, home_subsession_id, home_id, room_id, sensor_id);