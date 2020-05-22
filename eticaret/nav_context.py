from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout


from products.models import Category, Product
#from page.models import Page
#from page.views import STATUS

from orders.models import (
    ShopCart,

)

# Kategori ve Sepet Tutarı ve Ürünlerin her HTML sayfada gözükmesi için Kullanılıyor

def nav_data(request):
    context = dict()
    context['categories'] = Category.objects.all()

    #context['pages'] = Page.objects.filter(status=STATUS).order_by('title')
    return context


def price_data(request):
    context = dict()
    if request.user.is_authenticated:
        current_user=request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        context['cartotal'] = 0
        context['shopcart'] = shopcart
        if shopcart:
            carttotal=0
            for item in shopcart:
                carttotal += item.amount
            context['cartotal'] = carttotal
            context['shopcart'] = shopcart
        return context
    else:
        return context