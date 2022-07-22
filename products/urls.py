from django.urls import path

from products.views import ProductListView

urlpatterns = {
    path('/<int:category_id>', ProductListView.as_view()),
}