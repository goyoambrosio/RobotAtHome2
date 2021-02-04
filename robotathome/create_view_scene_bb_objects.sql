BEGIN TRANSACTION;

drop view if exists rh2_scene_bb_objects;
create view rh2_scene_bb_objects as
select * from rh_lblscene_bboxes
inner join rh_objects on rh_lblscene_bboxes.object_id=rh_objects.id;

COMMIT;
