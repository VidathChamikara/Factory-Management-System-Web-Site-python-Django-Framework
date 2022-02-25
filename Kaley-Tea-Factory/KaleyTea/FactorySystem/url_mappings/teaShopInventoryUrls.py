from django.urls import path
from FactorySystem.view_mappings import teaShopInventoryViews
from FactorySystem.view_mappings.teaShopInventoryViews import *

urlpatterns = [

    path('', teaShopInventoryViews.inventoryreports, name="inventoryhome"),

    path('Shop/InventoryHome/addCategoryProduct', teaShopInventoryViews.addCategoryProduct, name="addCategoryProduct"),
    path('Shop/InventoryHome/updateategoryProduct', teaShopInventoryViews.updateategoryProduct, name="updateategoryProduct"),
    path('Shop/InventoryHome/viewCategoryProduct', teaShopInventoryViews.viewCategoryProduct, name="viewCategoryProduct"),
    path('Shop/InventoryHome/deleteCategoryProduct', teaShopInventoryViews.deleteCategoryProduct, name="deleteCategoryProduct"),

    path('Shop/InventoryHome/addteapackets', teaShopInventoryViews.addteapackets, name="addteapackets"),
    path('Shop/InventoryHome/addteapackets/editpackets', teaShopInventoryViews.editpackets, name="editpackets"),
    path('Shop/InventoryHome/addteapackets/Updatepackets', teaShopInventoryViews.updatePackets, name="updatepackets"),
    path('Shop/InventoryHome/addteapackets/deletepackets', teaShopInventoryViews.deletepackets, name="deletepackets"),
    path('Shop/InventoryHome/viewpackets', teaShopInventoryViews.viewpackets, name="viewpackets"),

    path('Shop/InventoryHome/availableStock', teaShopInventoryViews.availableStock, name="availableStock"),

    path('Shop/InventoryHome/inventoryreports', teaShopInventoryViews.inventoryreports, name="inventoryreports"),
    path('Shop/InventoryHome/inventoryreports/inventorymonthlyreport', teaShopInventoryViews.inventorymonthlyreport,name="monthlyreport"),
    path('Shop/InventoryHome/inventoryreports/GenerateStockMothlyReport', GenerateStockMothlyReport.as_view(),name="GenerateStockMothlyReport"),
    path('Shop/InventoryHome/inventoryreports/GenerateStockAnnualReport', GenerateStockAnnualReport.as_view(),name="GenerateStockAnnualReport"),
    path('Shop/InventoryHome/inventoryreports/inventoryannualreport', teaShopInventoryViews.inventoryannualreport, name="annualreport"),

]
