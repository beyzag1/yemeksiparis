from django.urls import path
from yemekke.api import views as api_views
from .views import ProductCategoryAPIView,SellerUserAPIView,ProductAPIView,OrderAPIView,UserProfileAPIView

urlpatterns = [
    path('user-profile/',api_views.UserProfileAPIView.as_view(),name='customer-profile'),
    path('seller-profile/',api_views.SellerProfileAPIView.as_view(),name='restoran-profile'),
    path('categories/', ProductCategoryAPIView.as_view()),
    path('seller-users/', SellerUserAPIView.as_view()),
    path('seller-users/<int:pk>/', SellerUserAPIView.as_view()),
    path('products/', ProductAPIView.as_view()),
    path('products/<int:pk>/', ProductAPIView.as_view()),
    path('product/create',api_views.ProductCreateAPIView.as_view(),name='product-create'),
    path('orders/',api_views.OrderAPIView.as_view(),name='orders'),
    path('orders/<int:pk>',api_views.SingleOrderView.as_view(),name='orders-detail'),

]
