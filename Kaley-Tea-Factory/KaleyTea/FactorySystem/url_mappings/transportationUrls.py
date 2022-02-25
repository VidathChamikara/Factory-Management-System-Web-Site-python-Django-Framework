from django.urls import path
from FactorySystem.view_mappings import transportationViews
from FactorySystem.view_mappings.transportationViews import *

urlpatterns = [

    # transport management

    # Driver
    path('', transportationViews.driver_records, name="Transport"),
    path('UpdateDriver', transportationViews.DisplayDriverRecord, name="ShowDriver"),
    path('DeleteDriverRecords', transportationViews.deleteDriverRecord, name="delete_Driver_record"),
    path('Records', transportationViews.UpdateDriverRecord, name="update_Driver_record"),

    # Vehicle
    path('AddVehicle', transportationViews.Vehicle_Records, name="addVehicle"),
    path('DeleteVehicleRecords', transportationViews.deleteVehicleRecord, name="delete_record"),

    # Driving records
    path('DrivingRecords', transportationViews.DrivingRecords, name="vehicle_records"),
    path('ShowRecords', transportationViews.ShowDrivingRecords, name="RecordTable"),
    path('DeleteRecords', transportationViews.deleteRecords, name="delete_driving_records"),


    # vehicle repairs
    path('VehicleRepairs', transportationViews.AddVehicleRepairs, name="VehicleRepairs"),
    path('ShowVehicleRepairs', transportationViews.ShowVehicleRepairs, name="RepairTable"),
    path('EditVehicleRepairs', transportationViews.DisplayUpdateRepairs, name="show_repair_records"),

    path('UpdateVehicleRepairs', transportationViews.UpdateVehicleRepairs, name="update_repair_records"),
    path('deleteVehicleRepairs', transportationViews.delete_RepairRecords, name="delete_repair_records"),

    # reports
    path('Analysis', transportationViews.Reports, name="Reports"),
    path('Analysis/VehicleRecordsPDF', GenerateVehicle_RecordsPdf.as_view(), name="VehicleReports"),
    path('Analysis/VehicleRepairsPDF', GenerateVehicle_RepairPdf.as_view(), name="ServiceReports"),

    # search
    path('Analysis/Search', transportationViews.SearchRecords, name="searchRecords"),

]
