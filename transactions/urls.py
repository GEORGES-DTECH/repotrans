from django.urls import path

from . import views
from .views import (
    TransactionHomeView,
    TransactionUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
    SearchResultView,
   

    
    CylinderHomeView,
    CylinderUpdateView,
    CylinderCreateView,
    CylinderDeleteView,

    SaleHomeView,
    SaleUpdateView,
    SaleCreateView,
    SaleDeleteView,
  SalesearchResultView
  
)


urlpatterns = [
    

    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('transaction/new/', TransactionCreateView.as_view(),
         name='transaction_create'),
    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction_update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction_delete'),
    path('search/',SearchResultView.as_view(), name='search_results'),

   
   
    path('cylinders/', CylinderHomeView.as_view(), name='cylinder_home'),
    path('cylinder/new/', CylinderCreateView.as_view(),
         name='cylinder_create'),
    path('cylinder/<int:pk>/update/',
         CylinderUpdateView.as_view(), name='cylinder_update'),
    path('cylinder/<int:pk>/delete/',
         CylinderDeleteView.as_view(), name='cylinder_delete'),
     

    path('sales/', SaleHomeView.as_view(), name='sales_home'),
    path('sale/new/', SaleCreateView.as_view(),
         name='sales_create'),
    path('sale/<int:pk>/update/',
         SaleUpdateView.as_view(), name='sales_update'),
    path('sale/<int:pk>/delete/',
         SaleDeleteView.as_view(), name='sales_delete'),
  path('transactions/sale/search/',SalesearchResultView.as_view(),name='sale_search'),     

 

]
