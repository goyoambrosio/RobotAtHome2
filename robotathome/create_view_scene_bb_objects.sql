-- create a view that combines bounding boxes from 3D scenes with characterized 
-- objects from those bounding boxes
drop view if exists scene_bb_objects;
create view scene_bb_objects as 
select * from lblscene_bboxes 
inner join objects on lblscene_bboxes.object_id=objects.id;