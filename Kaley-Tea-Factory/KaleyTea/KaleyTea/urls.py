from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ------------ Common Urls ----------------------
    path('', include('common.urls'), name="home"),
    path('admin/', admin.site.urls),


    # --------- Salary-Nadeesh
    path('Employee/Salary/', include('FactorySystem.url_mappings.SalaryUrls')),
  

    # ------ OutletSalesUrls ------
    path('Shop/Outlet/', include('FactorySystem.url_mappings.outletSalesUrls')),
  
    
  # ------ TeaShopInventoryUrls -------
    path('Shop/InventoryHome', include('FactorySystem.url_mappings.teaShopInventoryUrls')),
    path('Factory/Transport/', include("FactorySystem.url_mappings.transportationUrls")),

  
    # ----- employeeManagementUrls ------
    path('Factory/EmployeeHome/', include('FactorySystem.url_mappings.employeeManagementUrls')),

  
    # ----- Inventory ----
    path('', include('dashboard.urls')),
    path('', include('user.urls')),
  
  
    # ----- AuctionStocksUrls ------
    path('sub/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('allcat/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('cat/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('editAuction/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('updateAuction/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('deleteAuction/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('bb/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('Registration/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('Read/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('edit/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('update/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('editnew/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('updatenew/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('addBuyer/', include('FactorySystem.url_mappings.auctionStocksUrls')),

    path('buyerDetailsPDF/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('currentStockPDF/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    #path('ReadbuyerDetailsPDF/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    #path('editbuyerDetailsPDF/', include('FactorySystem.url_mappings.auctionStocksUrls')),

    path('BuyerRead/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('editBuyer/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('updateBuyer/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('deleteBuyer/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('stock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('soldstock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('notsoldstock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('editStock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('readSoldStock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('editnotSoldStock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('readnotSoldStock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
    path('deleteCurrentStock/', include('FactorySystem.url_mappings.auctionStocksUrls')),
  
  
    # ------ Supplier -------
    path('Supplier/Reg/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Upanddel/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Payment/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Addleaf/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Paydetails/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Leafstock/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Regdetails/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Edit/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Supplier/Update/', include('FactorySystem.url_mappings.supplierUrls')),
    path('supplierTrial/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Read/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Edit/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Update/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Payment/Delete/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Trial/Delete/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Sup/Delete/', include('FactorySystem.url_mappings.supplierUrls')),
    path('Leaf/Delete/', include('FactorySystem.url_mappings.supplierUrls')),
    path('suppayDetailsPDF/', include('FactorySystem.url_mappings.supplierUrls')),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
