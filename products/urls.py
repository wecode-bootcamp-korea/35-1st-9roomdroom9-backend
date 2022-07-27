from django.urls import path

from products.views import MainPageView, ProductListView, ProductDetailView

urlpatterns = {
    path('/main', MainPageView.as_view()),
    path('/<int:category_id>', ProductListView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
}