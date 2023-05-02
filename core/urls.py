from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('product/create-or-update/', views.ProductCreate.as_view(), name='product_create_update'),

    path('category/list/', views.CategoryList.as_view(), name='category_list'),
    path('product/list/', views.ProductList.as_view(), name='product_list'),
    path('product/redirect/', views.ProductRedirect.as_view(), name='product_redirect'),
    path('product/price-change/list/', views.PriceChangeList.as_view(), name='product_price_change_list'),
]
