drop view if exists scene_bb_objects;
create view scene_bb_objects as 
select * from lblscene_bboxes 
inner join objects on lblscene_bboxes.object_id=objects.id;