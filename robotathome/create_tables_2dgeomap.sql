BEGIN TRANSACTION;

------------------------------------------------------
--                  RH_TWODGEOMAP                   --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_twodgeomap`;
CREATE TABLE IF NOT EXISTS `rh_twodgeomap` (
	`id`	integer NOT NULL UNIQUE,
	`home_id`	integer,
	`room_id`	integer,
	`x`	real,
	`y`	real,
	`z`	real,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`room_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`)
);

-- Indexes for rh_twodgeomap
DROP INDEX IF EXISTS idx_twodgeomap_room_id;
CREATE INDEX idx_twodgeomap_room_id ON rh_twodgeomap(room_id);
DROP INDEX IF EXISTS idx_twodgeomap_home_id;
CREATE INDEX idx_twodgeomap_home_id ON rh_twodgeomap(home_id);


COMMIT;
