from django.urls import path

from .views import (
    post_index,
    post_detail,
)

app_name='post'
urlpatterns=[
    path('', post_index, name='blogpage'),
    # Dinamik URL ler
    path('<slug:slug>/', post_detail, name='detail'),

]