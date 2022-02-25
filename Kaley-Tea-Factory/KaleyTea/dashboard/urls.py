from django.urls import path
from . import views

urlpatterns = [
    path('make/request/', views.make_request, name='dashboard-make-request'),
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('product/', views.product, name='dashboard-product'),
    path('product/delete/', views.product_delete, name='dashboardProductDelete'),
    path('product/update/', views.product_update, name='dashboardProductUpdate'),
    # path('product/report/', views.product_report, name='dashboardProductReport'),
    path('product/view/', views.product_view, name='dashboardProductView'),
    path('order/', views.order, name='dashboard-order'),
    path('product/updateLeaf/', views.updateLeaf, name="updateLeaf"),
    path('product/', views.NavigateToPrevInv, name="NavigateToPrevInv"),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('PreviousInventories/UpdateInvenories', views.NavigateToUpdateInv, name="NavigateToUpdateInv"),
    path('PreviousInventories/InventoryReport', views.NavigateToInvReport, name="NavigateToInvReport"),

    # Leaf inventory Daily Production
    path('DailyProduction', views.NavigateToProduction, name="final_production_home"),
    path('AddMainProduction', views.addMainFinalProduction, name="addMainFinalProduct"),
    path('deleteSubProdAll', views.deleteSubProd, name="deleteSubProdAll"),
    path('CustomDailyProduction', views.NavigateToCustomDailyProd, name="NavigateToCustomDailyProd"),
    path('CustomDailyProduction/subDel', views.NavigateToDelSubPr, name="delete_sub"),
    path('CustomDailyProduction/ViewProduct', views.NavigateToViewProduct, name="NavigateToViewProd"),
    path('TeaGrades', views.NavigateToTeaGrades, name="NavigateToTeaGrades"),
    path('TeaGrades/Delete', views.DeleteGrade, name="deleteGrade"),

]
