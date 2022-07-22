from django.urls import path

from products.views import ProductListView, ProductDetailView

urlpatterns = {
    path('/<int:category_id>', ProductListView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
}