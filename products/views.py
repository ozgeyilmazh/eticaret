from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse

# Create your views here.
from products.models import (
    Category,
    Product,
    STATUS,
    DEFAULT_STATUS,
    Comment)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from products.forms import SearchForm, CommentForm
from orders.forms import ShopCartForm
import json


# ÜRÜN LİSTELEME
def productIndex(request):
    context = dict()
    context['items'] = Product.objects.all().order_by("-pk")

    query = request.GET.get('q')
    if query:
        context['items'] = context['items'] .filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(context['items'], 8)

    page = request.GET.get('page')

    context['items'] = paginator.get_page(page)

    template = 'products/shop.html'
    return render(request, template, context)


# ÜRÜN DETAY
def productDetail(request, id):
    context = dict()
    url = request.META.get('HTTP_REFERER')
    context['form'] = ShopCartForm()
    context['products'] = Product.objects.order_by("-pk")[:4]
    try:
        context['items'] = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise Http404("Product yok ")
    context['form2'] = CommentForm(request.POST or None)

    productPost = get_object_or_404(Product, pk=id)
    if context['form2'].is_valid():
        comment = context['form2'].save(commit=False)
        comment.productPost = productPost
        comment.save()
        return HttpResponseRedirect(url)

    counts = Comment.objects.filter(productPost=id, approved_comment=True)

    a = 0
    for i in counts:
        a += 1

    context['commentsCount'] = a
    #print(context['commentsCount'])

    template = 'products/product-detail.html'
    return render(request, template, context)


# PAGINATOR - KATEGORİ ANASAYFADAKİ DROP-DOWN Listeleme
def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category,
        slug=category_slug,

    )

    # NAV:
    # context['categories'] = Category.objects.filter(status=STATUS).order_by('title')
    context['items'] = Product.objects.filter(
        category=context['category'],
    )
    paginator = Paginator(context['items'], 8)

    page=request.GET.get('page')

    context['items'] = paginator.get_page(page)

    template = 'products/category_show.html'
    return render(request, template, context)


# ÜRÜN ARAMA
def product_search(request):
    context=dict()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            context['category']=Category.objects.all()
            search_query=form.cleaned_data['search_query']
            context['products']=Product.objects.filter(title__icontains=search_query)
            return render(request, 'products/products_search.html', context)

    return HttpResponseRedirect('/')


# ÜRÜN ARAMA
def product_search_auto(request):
    if request.is_ajax():
        query=request.GET.get('term', '')
        product=Product.objects.filter(title__icontains=query)
        results=[]
        for item in product:
            product_json={}
            product_json=item.title
            results.append(product_json)
        data=json.dumps(results)

    else:
        data="fail"
    mimetype="application/json"
    return HttpResponse(data, mimetype)


# ÜRÜN YORUM VIEW
@login_required(login_url="login")
def add_comment_to_post(request, pk):
    productPost = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.productPost = productPost
            comment.save()
            return redirect('products/product.html', pk=productPost.pk)
    else:
        form = CommentForm()
    return render(request, 'products/comments.html', {'form': form})


# YORUM ONAYLAMA
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    return redirect('products/product-detail.html', pk=comment.productPost.pk)

# YORUM SİLME
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('products/product-detail.html', pk=comment.productPost.pk)