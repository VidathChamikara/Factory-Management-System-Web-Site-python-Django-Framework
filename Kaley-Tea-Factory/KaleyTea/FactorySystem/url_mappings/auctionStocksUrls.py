from django.urls import path
from FactorySystem.view_mappings import auctionStocksViews

urlpatterns = [

    path('addSub/', auctionStocksViews.addSubStock),
    path('all/', auctionStocksViews.readAuction),
    path('cat/', auctionStocksViews.addAuction),
    path('editAuctionStock/<int:id>', auctionStocksViews.editAuction),
    path('updateAuctionStock/<int:id>', auctionStocksViews.updateAuction),
    path('deleteAuction/<int:id>', auctionStocksViews.deleteAuction),
    path('aa/', auctionStocksViews.Indexpage),
    path('Registration/', auctionStocksViews.Userreg),
    path('Read/', auctionStocksViews.RegRead),
    path('edit/<int:id>', auctionStocksViews.editemp),
    path('update/<int:id>', auctionStocksViews.updateemp),
    path('addBuyer/', auctionStocksViews.AddNewBuyer),

    path('buyerDetailsPDF/', auctionStocksViews.generateReport),
    path('currentStockPDF/', auctionStocksViews.generateReportStock),


    #path('ReadbuyerDetailsPDF/', auctionStocksViews.BuyerReadPDF),
    #path('editbuyerDetailsPDF/<int:id>', auctionStocksViews.editBuyerPDF),

    path('BuyerRead/', auctionStocksViews.BuyerRead),
    path('editBuyer/<int:id>', auctionStocksViews.editBuyer),
    path('updateBuyer/<int:id>', auctionStocksViews.updateBuyer),
    path('updateBuyer/<int:id>', auctionStocksViews.deleteBuyer),
    path('deleteBuyer/<int:id>', auctionStocksViews.deleteBuyer),
    path('stock/', auctionStocksViews.readStock),
    path('soldstock/<int:id>', auctionStocksViews.SoldStock),
    path('editStock/<int:id>', auctionStocksViews.editStock),
    path('readSoldStock/', auctionStocksViews.readSoldStock),
    path('editnotSoldStock/<int:id>', auctionStocksViews.editnotSoldStock),
    path('notsoldstock/<int:id>', auctionStocksViews.notSoldStock),
    path('readnotSoldStock/', auctionStocksViews.readnotSoldStock),
    path('deleteCurrentStock/<int:id>', auctionStocksViews.deleteCurrentStock),
]