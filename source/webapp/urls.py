from django.contrib import admin
from django.urls import path
from .views import (
                    ProductList,
                    ProductView,
                    ProductEdit,
                    ProductDelete,
                    ProductCreate,
                    ReviewCreate,
                    ReviewEdit,
                    ReviewDelete
                    )

app_name = 'webapp'

urlpatterns = [
    path('', ProductList.as_view(), name='main_page'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/<int:pk>/edit/', ProductEdit.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('product/create_product/', ProductCreate.as_view(), name='product_create'),
    path('review/<int:pk>/create/', ReviewCreate.as_view(), name='review_create'),
    path('review/<int:pk>/edit/', ReviewEdit.as_view(), name='review_edit'),
    path('review/<int:pk>/<int:id>/delete/', ReviewDelete.as_view(), name='review_delete')
]