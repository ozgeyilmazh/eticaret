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


import iyzipay
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.urls import reverse


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


api_key = 'sandbox-etkBOaBAec7Zh6jLDL59Gng0xJV2o1tV'
secret_key = 'sandbox-uC9ysXfBn2syo7ZMOW2ywhYoc9z9hTHh'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}


sozlukToken = list()


def payment(request):
    context = dict()

    sepet = ShopCart.objects.all()
    odeme = list()
    for i in sepet:
        odeme.append(i.user)
        odeme.append(i.product)
        odeme.append(i.quantity * i.product.salePrice)
        print("------------", odeme)

    buyer = {
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address = {
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items = [
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '50.0'
        },

    ]


    # conversationId bunun için time modülü ile anlık değer üretiyorum. Yolluyorum.
    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': odeme[2],
        'paidPrice': odeme[2],
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://localhost:8007/orders/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        #'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print("------------------------")
    print(json_content)
    print("------------------------")
    print("gelen veri tipi", type(json_content))
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


    #print(json_content["checkoutFormContent"])
    #context['payment'] = json_content["checkoutFormContent"]
    #template = 'payment.html'
    #return render(request, template, context)


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('order_index')
    print("result içindeki token -----", sozlukToken)
    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)


def success(request):
    context = dict()
    context['success'] = 'İşlem Başarılı'

    template = 'payment/ok.html'
    return render(request, template, context)


def failure(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'

    template = 'payment/fail.html'
    return render(request, template, context)

