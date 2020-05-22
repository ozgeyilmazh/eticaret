from django.shortcuts import render
from .models import About, Contact

from products.models import Product
# Create your views here.
from django.http import HttpResponseRedirect

def index(request):
    context = dict()
    context['is_home_products'] = Product.objects.all()
    return render(request, 'index.html', context)


def about(request):
    context = dict()
    context['about'] = About.objects.all()
    return render(request, 'about.html', context)

def contact(request):
    context = dict()
    context['contact'] = Contact.objects.all()

    return render(request, 'contact.html', context)