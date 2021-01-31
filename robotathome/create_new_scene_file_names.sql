-- Create an auxiliary table called scene_files table to store 
-- new file names for scene files.
-- The purpose is to gather all the files under the same folder to make the new 
-- dataset version independent from the old one.
-- Scene files from labelled scenes are not considered because they are the same
-- files but with added information about objects and bounding boxes. Tha information
-- has neen stored in lblscene_bboxes table.

drop table if exists scenes_files;
create table scenes_files as
select 
    rctrscene.id, 
	homes.name home_name,
	substr(rooms.name,instr(rooms.name,"_")+1) room_name,
	rctrscene.home_session_id home_session,
	rctrscene.home_subsession_id home_subsession,
		scene_file
from rctrscene
inner join homes on homes.id=rctrscene.home_id
inner join rooms on rooms.id=rctrscene.room_id;

update scenes_files
set scene_file = id || "_scene.txt";

drop table if exists old2new_scene_files;
create table old2new_scene_files as
select 
    rctrscene.id id, 
    rctrscene.scene_file old_file,
	"session_"|| (scenes_files.home_session + 1) || "/" ||
	    scenes_files.home_name || "/" || 
	   scenes_files.room_name || "/" ||
	    "subsession_" || (scenes_files.home_subsession + 1)  new_path,	
    scenes_files.scene_file new_file
from 
    rctrscene 
inner join scenes_files on rctrscene.id = scenes_files.id;

drop table if exists scenes_files;