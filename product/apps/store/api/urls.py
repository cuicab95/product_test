from django.urls import path

from rest_framework import routers

from . import views


app_name = 'api'

router = routers.SimpleRouter()
urlpatterns = [
    path('v1/create-order/', views.CreateOrderView.as_view(), name='create-order'),

] + router.urls

