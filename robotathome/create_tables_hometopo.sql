BEGIN TRANSACTION;

------------------------------------------------------
--                  RH_HOMETOPO                     --
------------------------------------------------------
DROP TABLE IF EXISTS `rh_hometopo`;
CREATE TABLE IF NOT EXISTS `rh_hometopo` (
	`id`	integer NOT NULL UNIQUE,
	`home_id`	integer,
	`room1_id`	integer,
	`room2_id`	integer,
	FOREIGN KEY(`room1_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`room2_id`) REFERENCES `rh_rooms`(`id`),
	FOREIGN KEY(`home_id`) REFERENCES `rh_homes`(`id`),
	PRIMARY KEY(`id`)
);

-- Indexes for rh_hometopo
DROP INDEX IF EXISTS idx_hometopo_home_id;
CREATE INDEX idx_hometopo_home_id ON rh_hometopo(home_id);
DROP INDEX IF EXISTS idx_hometopo_room1_id;
CREATE INDEX idx_hometopo_room1_id ON rh_hometopo(room1_id);
DROP INDEX IF EXISTS idx_hometopo_room2_id;
CREATE INDEX idx_hometopo_room2_id ON rh_hometopo(room2_id);

COMMIT;
