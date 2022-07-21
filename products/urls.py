from django.urls import path

from products.views import ProductListView

urlpatterns = {
    path('', ProductListView.as_view()),
    path('/<int:cat_id>', ProductListView.as_view()),
}