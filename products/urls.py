from django.urls import path

from products.views import ProductListView

urlpatterns = {
    path('/list', ProductListView.as_view()),
}