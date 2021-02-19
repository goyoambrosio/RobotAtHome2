drop table if exists temp.rgbd_1;
create TEMPORARY table rgbd_1 as
select f2, pth from rh2_lblrgbd
where rh2_lblrgbd.s_name = 'RGBD_1';

drop table if exists temp.rgbd_2;
create TEMPORARY table rgbd_2 as
select f2 from rh2_lblrgbd
where rh2_lblrgbd.s_name = 'RGBD_2';

drop table if exists temp.rgbd_3;
create TEMPORARY table rgbd_3 as
select f2 from rh2_lblrgbd
where rh2_lblrgbd.s_name = 'RGBD_3';

drop table if exists temp.rgbd_4;
create TEMPORARY table rgbd_4 as
select f2 from rh2_lblrgbd
where rh2_lblrgbd.s_name = 'RGBD_4';

drop view if exists temp.rgbd_1234;
create TEMPORARY view rgbd_1234 as
SELECT temp.rgbd_1.f2, temp.rgbd_2.f2, temp.rgbd_3.f2, temp.rgbd_4.f2, temp.rgbd_1.pth
FROM temp.rgbd_1, temp.rgbd_2, temp.rgbd_3, temp.rgbd_4
where 
    temp.rgbd_1.rowid = temp.rgbd_2.rowid AND
	temp.rgbd_1.rowid = temp.rgbd_3.rowid AND
	temp.rgbd_1.rowid = temp.rgbd_4.rowid;