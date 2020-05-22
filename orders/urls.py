from django.urls import path
from .views import (
    shop_cart_add,
    shop_cart_delete,
    shop_cart_list,
    shop_cart_checkout,
    order_detail,
    index,
    user_login,
)


urlpatterns = [
    path('', user_login, name='user_login'),
    path('order_index/', index, name='order_index'),
    path('shopcart/', shop_cart_list, name='shopcart'),
    path('addtocart/<int:pid>', shop_cart_add, name='addtocart'),
    path('deletefromcart/<int:id>/', shop_cart_delete, name='deletefromcart'),
    path('detail/<int:id>/', order_detail, name='order_detail'),
    path('checkout/', shop_cart_checkout, name='checkout'),

]