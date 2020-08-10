
from django.contrib import admin
from django.urls import path, include
from . import settings
from transactions.views import TransactionHomeView

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TransactionHomeView.as_view(), name='transaction_home'),
    path('transactions/',include('transactions.urls')),
    path('accounts/', include('accounts.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
