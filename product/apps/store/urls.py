from django.urls import path, include

app_name = 'store'

urlpatterns = [
    path('api/', include('product.apps.store.api.urls'))
]

