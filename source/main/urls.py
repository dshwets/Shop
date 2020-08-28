"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.views import IndexView, WatchProductView, CreateProduct, \
    UpdateProductView, DeleteProductView,WatchCart,AddProductToCart,DeleteCart, CreateOrder

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', WatchProductView.as_view(), name='watch_product'),
    path('product/add/', CreateProduct.as_view(), name='create_product'),
    path('product/<int:pk>/update/', UpdateProductView.as_view(), name='update_product'),
    path('product/<int:pk>/delete/', DeleteProductView.as_view(), name='product_delete'),

    path('cart/', WatchCart.as_view(), name='watch_cart'),
    path('cart/add/<int:pk>/', AddProductToCart.as_view(), name='add_to_cart'),
    path('cart/delete/<int:pk>/',DeleteCart.as_view(), name = 'delete_cart'),
    path('cart/make_cart', CreateOrder.as_view(), name = 'make_order'),
]
