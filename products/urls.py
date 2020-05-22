from django.urls import path
from .views import (
    productIndex,
    productDetail,
    category_show,

# ÜRÜN YORUM URL
    add_comment_to_post,
    comment_approve,
    comment_remove,

)


urlpatterns = [
    path('', productIndex, name='products'),
    path('detail/<int:id>/', productDetail, name='productDetail'),
    path('<slug:category_slug>', category_show, name="category_show"),


    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
]