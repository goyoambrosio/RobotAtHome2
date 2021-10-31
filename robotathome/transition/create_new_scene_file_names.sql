-- Create an auxiliary table called scene_files table to store
-- new file names for scene files.
-- The purpose is to gather all the files under the same folder to make the new
-- dataset version independent from the old one.
-- Scene files from labelled scenes are not considered because they are the same
-- files but with added information about objects and bounding boxes. Tha information
-- has neen stored in lblscene_bboxes table.

BEGIN TRANSACTION;

drop table if exists rh2_scene_files;
create table rh2_scene_files as
select
    rh_rctrscene.id,
	rh_homes.name home_name,
	substr(rh_rooms.name,instr(rh_rooms.name,"_")+1) room_name,
	rh_rctrscene.home_session_id home_session,
	rh_rctrscene.home_subsession_id home_subsession,
	rh_rctrscene.scene_file
from rh_rctrscene
inner join rh_homes on rh_homes.id=rh_rctrscene.home_id
inner join rh_rooms on rh_rooms.id=rh_rctrscene.room_id;

update rh2_scene_files
set scene_file = id || "_scene.txt";

drop table if exists rh2_old2new_scene_files;
create table rh2_old2new_scene_files as
select
    rh_rctrscene.id id,
    rh_rctrscene.scene_file old_file,
	"session_"|| (rh2_scene_files.home_session + 1) || "/" ||
	    rh2_scene_files.home_name || "/" ||
	    rh2_scene_files.room_name || "/" ||
	    "subsession_" || (rh2_scene_files.home_subsession + 1)  new_path,
    rh2_scene_files.scene_file new_file
from
    rh_rctrscene
inner join rh2_scene_files on rh_rctrscene.id = rh2_scene_files.id;

-- Indexes for rh2_old2new_scene_files
DROP INDEX IF EXISTS idx_scene_file;
CREATE INDEX idx_scene_file ON rh2_old2new_scene_files (new_file);

drop table if exists rh2_scene_files;

COMMIT;
