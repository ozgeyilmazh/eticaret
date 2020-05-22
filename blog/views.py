from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post

from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# BLOG POST LİSTELEME
def post_index(request):
    context = dict()
    post_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 4)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        context['posts'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context['posts'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        context['posts'] = paginator.page(paginator.num_pages)

    template = 'blog/blog.html'
    return render(request, template, context)


# BLOG POST DETAY SAYFASI
def post_detail(request, slug):
    context = dict()
    context['post'] = get_object_or_404(Post, slug=slug)

    template = 'blog/single-blog.html'
    return render(request, template, context)