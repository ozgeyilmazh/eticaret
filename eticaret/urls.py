"""eticaret URL Configuration

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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from products.views import product_search,product_search_auto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('page.urls')),
    path('blog/', include('blog.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
        # ÜRÜN ARAMA URL
    path('search/', product_search, name="product_search"),
    path('search_auto/', product_search_auto, name="product_search_auto"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)