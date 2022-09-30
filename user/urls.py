from django.urls import path,include

from . import views
from rest_framework import routers
from rest_framework.authtoken import views as v
router = routers.DefaultRouter()
router.register('user', views.userviewsets)

urlpatterns = [
    path('', views.index),
    path('login',views.login),
    path('logout',views.logout),
    path('api/', include(router.urls)),
    path('api-token-auth/', v.obtain_auth_token, name='api-token-auth'),
    path('user/registration',views.loadUserRegistration),
    path('user/addUser',views.addUser),
    path('user/validateUser',views.validateUser),
    path('user/shop',views.shop),
    path('user/shop/product/<product_id>',views.detaiPage),
    path('user/shop/product/category/<category_id>',views.categoryPage),
    path('user/shop/addToCart',views.addToCart),
    path('user/shop/cart',views.loadCart,name='loadCart'),
    path('user/shop/product/delete/<cart_id>',views.deleteCart)

]