from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track-order/', views.track_order, name='track_order'),
    path('special-order/', views.special_order, name='special_order'),
]