from django.urls import path, include

urlpatterns = [
    path('', include('main.urls'))
    path('products', include('products.urls'))
]