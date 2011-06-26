CONSTRAINT FK_VehicleMaintenance_Vehicle FOREIGN KEY
	IX_VehicleMaintenance_VehicleId (VehicleId)
	REFERENCES Vehicle (Id);

CONSTRAINT FK_VehicleMaintenance_MaintenanceType FOREIGN KEY
	IX_VehicleMaintenance_MaintenanceTypeId (MaintenanceTypeId)
	REFERENCES MaintenanceType (Id);
