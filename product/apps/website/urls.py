from django.urls import path, include
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('order/<int:order_id>/detail/', views.OrderDetailView.as_view(), name='order-detail'),
]

