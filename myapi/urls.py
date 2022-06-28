from django.urls import path
from .views import *


urlpatterns = [

    # User
    path('token/', LoginView.as_view(), name='token'),
    path('refetch-token/', RefreshTokenView.as_view(), name='refetch-token'),
    path('register/', RegisterApiView().as_view(), name='register'),

    # Product
    path('categories/', CategoryGenericsView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetail.as_view(),
         name='product-detail'),

    # Cart
    path('carts/', CartList.as_view(), name='carts'),
    path('cart/<int:pk>/', CartUpdate.as_view(), name='cart-update'),
    path('cart/<int:cart_id>/<int:product_id>/',
         CartDestroy.as_view(), name='cart-destroy'),

    # contact
    path('contact/', ContactCreate.as_view(), name='contact'),
]
