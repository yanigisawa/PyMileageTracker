CREATE TABLE `VehicleMaintenance` (
`id` INTEGER NOT NULL AUTO_INCREMENT DEFAULT NULL ,
`VehicleId` INTEGER NOT NULL DEFAULT 0 ,
`MaintenanceTypeId` INTEGER NOT NULL DEFAULT 0 ,
`Date` DATETIME NOT NULL DEFAULT '1900-01-01' ,
`Odometer` DECIMAL(20,3) DEFAULT NULL ,
`FillUpMileage` DECIMAL(10,3) DEFAULT NULL ,
`FillUpGallons` DECIMAL(10,3) DEFAULT NULL ,
`FillUpCostPerGallon` DECIMAL(10,2) DEFAULT NULL ,
PRIMARY KEY (`id`)
) COMMENT='Table to store maintenance types for the given vehicle';

ALTER TABLE `VehicleMaintenance` ADD FOREIGN KEY (VehicleId) REFERENCES `Vehicle` (`id`);
ALTER TABLE `VehicleMaintenance` ADD FOREIGN KEY (MaintenanceTypeId) REFERENCES `MaintenanceType` (`id`);
