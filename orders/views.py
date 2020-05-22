from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse

from .models import (
    ShopCart,
    User,
    Order,
    OrderDetail,
)
from .forms import ShopCartForm, OrderForm

# Sipariş Listeleme
@login_required(login_url="login")
def index(request):
    context = dict()

    current_user = request.user
    orders = Order.objects.all().filter(user_id=current_user.id)
    request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count()
    context['page'] = 'orders'
    context['orders'] = orders

    return render(request, 'orders/order-list.html', context)


def user_login(request):
    context = dict()

    current_user = request.user
    orders = Order.objects.all().filter(user_id=current_user.id)
    request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count()
    context['page'] = 'orders'
    context['orders'] = orders

    return render(request, 'orders/user_login.html', context)

# Sepete ürün Ekliyor
@login_required(login_url="login")
def shop_cart_add(request, pid):
    url = request.META.get('HTTP_REFERER')
    form = ShopCartForm(request.POST or None)
    print(form)
    if request.method == 'POST':
        print(request.method)
        if form.is_valid():
            current_user = request.user
            #quantity = form.clearned_data['quantity']
            quantity = form.cleaned_data['quantity']
            print(quantity)
            try:
                q1 = ShopCart.objects.get(user_id=current_user.id, product_id=pid)
            except ShopCart.DoesNotExist:
                q1 = None
            if q1 != None:
                q1.quantity = q1.quantity + quantity
                q1.save()
            else:
                data = ShopCart(user_id=current_user.id, product_id=pid, quantity=quantity)
                data.save()
            # Sepetin üstünde aktif ürün sayıyı gösterimi
            request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
            messages.success(request, "Product add to cart..")
            return HttpResponseRedirect(url)
            print("burası son")
    return HttpResponseRedirect(reverse('shopcart', args=None))


# Sepetteki ürünleri ve fiyatları listeliyor
@login_required(login_url="login")
def shop_cart_list(request):
    context = dict()
    quantity = 1
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    carttotal = 0
    for item in shopcart:
        carttotal += item.quantity * item.product.salePrice
    context['carttotal'] = carttotal
    context['shopcart'] = shopcart

    return render(request, 'orders/shopping-cart.html', context)


# Sepetten Ürün Silme
@login_required(login_url="login")
def shop_cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "Prodcut deleted from .. ")
    return HttpResponseRedirect(url)


# Müşteri Sepet Onaylama
@login_required(login_url="login")
def shop_cart_checkout(request):
    context = dict()
    current_user = request.user
    # Sistemdeki user sepet bilgisi shopcart= ...
    shopcart = ShopCart.objects.all().filter(user_id=current_user.id)
    carttotal = 0
    for rs in shopcart:
        carttotal += rs.quantity * rs.product.price
    form = OrderForm(request.POST or None)
    print(form)
    if request.method == 'POST':
        if form.is_valid():
            # Eğer gerçek ödeme gelirse, bankadan gelen kısmı burada kontrol etmek gerekcek
            # Kart bilgileri bankaya gider ve sonuç alınır
            # if payment accepted continue else send payment error to checkout page
            data = Order()
            data.name = form.cleaned_data['name']
            print(data.name)
            data.surname = form.cleaned_data['surname']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.to = form.cleaned_data['name']
            data.user_id = current_user.id
            data.total = carttotal
            data.save()

            for rs in shopcart:
                detail = OrderDetail()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.total = rs.amount
                detail.save()
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, 'Order has been Completed. Thank You')
            return HttpResponseRedirect("/orders")

    context['page'] = 'checkout'
    context['shopcart'] = shopcart
    context['carttotal'] = carttotal

    return render(request, 'orders/checkout.html', context)


# Sipariş Detay
@login_required(login_url="login")
def order_detail(request, id):
    context = dict()
    print(id)
    order = Order.objects.get(pk=id)
    items = OrderDetail.objects.all().filter(order=id)


    context['page'] = 'detail'
    context['order'] = order
    context['items'] = items

    return render(request, 'orders/order-detail.html', context)