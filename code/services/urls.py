from django.urls import path
from .views import ServicesView,ServicesDetailView

urlpatterns = [
    path('', ServicesView.as_view(), name='services_list'),
    path('<slug:slug>/', ServicesDetailView.as_view(), name='service_detail'),
]
