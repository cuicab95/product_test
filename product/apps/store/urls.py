from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('api/', include('product.apps.store.api.urls'))
]

