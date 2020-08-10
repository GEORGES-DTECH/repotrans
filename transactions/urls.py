from django.urls import path
from . import views
from .views import (
    TransactionHomeView,
    TransactionUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
  
)


urlpatterns = [
    

    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('transaction/new/', TransactionCreateView.as_view(),
         name='transaction_create'),
    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction_update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction_delete'),



]
