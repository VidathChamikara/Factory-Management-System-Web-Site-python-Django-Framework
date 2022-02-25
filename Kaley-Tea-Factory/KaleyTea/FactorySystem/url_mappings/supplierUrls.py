from django.contrib import admin
from django.urls import path

from FactorySystem.view_mappings import supplierdetailsViews
urlpatterns = [

    path('supplierReg/', supplierdetailsViews.Supregdetails),
    path('supplierUpanddel/', supplierdetailsViews.supplierUpanddel),
    path('supplierPayment/', supplierdetailsViews.Paymentdetails),
    path('supplierAddleaf/', supplierdetailsViews.Leafstockdetails),
    path('supplierPaydetails/', supplierdetailsViews.Payread),
    path('supplierLeafstock/', supplierdetailsViews.Leafread),
    path('supplierRegdetails/', supplierdetailsViews.Regread),
    path('supplierEdit/<int:id>', supplierdetailsViews.Supedit),
    path('supplierUpdate/<int:id>', supplierdetailsViews.supupdate),
    path('supplierTrial/', supplierdetailsViews.Userreg),
    path('trialRead/', supplierdetailsViews.Trialread),
    path('trialEdit/<int:id>', supplierdetailsViews.editeemp),
    path('trialUpdate/<int:id>', supplierdetailsViews.update),
    path('paymentDelete/<int:id>', supplierdetailsViews.Paydelete),
    path('trialDelete/<int:id>', supplierdetailsViews.Trialdelete),
    path('supDelete/<int:id>', supplierdetailsViews.Supdelete),
    path('leafDelete/<int:id>', supplierdetailsViews.Leafdelete),
    path('suppayDetailsPDF/', supplierdetailsViews.generatepayment),





]
