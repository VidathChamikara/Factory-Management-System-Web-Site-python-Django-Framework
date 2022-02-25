from django.urls import path

from FactorySystem.view_mappings import outletSalesViews, outletSalesReportViews

urlpatterns = [
    # Price Table
    path('priceTable/', outletSalesViews.sales_price_table, name='price-table'),
    path('updatePrice/', outletSalesViews.update_product_price, name='update-price'),
    path('removePrice/', outletSalesViews.remove_product_price, name='remove-price'),

    # New Bill
    path('newBill/', outletSalesViews.new_bill, name='new-bill'),
    path('updateCart/', outletSalesViews.update_cart, name='update-cart'),
    path('removeFromCart/', outletSalesViews.remove_from_cart, name='remove-from-cart'),
    path('clearCart/', outletSalesViews.clear_cart, name='clear-cart'),
    path('checkout/', outletSalesViews.checkout, name='checkout'),

    # Transactions
    path('transactions/', outletSalesViews.transactions, name='transactions'),
    path('billDetails/id=<int:id>', outletSalesViews.view_bill_details, name='bill-details'),
    path('transactions/delete-bill-record/', outletSalesViews.delete_bill_details, name='delete-bill'),

    # Sales Reports
    path('sales-reports/', outletSalesViews.sales_reports, name='sales-reports'),

    # Generate PDFs
    path('billDetails/generate-bill/id=<int:id>', outletSalesReportViews.generate_bill, name='print-bill'),
    path('sales-reports/report-yesterday', outletSalesReportViews.report_yesterday, name='report-yesterday'),
    path('sales-reports/report-last-7-days', outletSalesReportViews.report_last_7_days, name='report-last7'),
    path('sales-reports/report-last-month', outletSalesReportViews.report_last_month, name='report-lastMonth'),
    path('sales-reports/report-last-year', outletSalesReportViews.report_last_year, name='report-lastYear'),
    path('sales-reports/report-specific-month', outletSalesReportViews.report_specific_month, name='report-specificMonth'),
    path('sales-reports/report-specific-year', outletSalesReportViews.report_specific_year, name='report-specificYear'),

]
