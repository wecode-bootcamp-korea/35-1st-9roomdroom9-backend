from django.urls import path

from .views import CartCreateView

urlpatterns = [
    path('/cart', CartCreateView.as_view()),
]