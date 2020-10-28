from django.shortcuts import render, get_object_or_404,redirect
from django.http  import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Category, Product,InstaRecap, Kategory
from cart.forms import CartAddProductForm
from random import sample
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from .forms import CommentForm

# Create your views here.
def welcome(request):
    return render(request, 'base.html', {})

def post_list_by_kategory(request , kategory_slug):
    kategories = Kategory.objects.all()
    post = Post.objects.filter(status='published')
    if kategory_slug:
        kategory = get_object_or_404(Kategory, slug=kategory_slug)
        post = post.filter(kategory=kategory)
    insta = InstaRecap.objects.all()[0:1]
    insta2 = InstaRecap.objects.all()[1:2]
    return render(request, 'blog/category/post_by_category.html', {'kategories': kategories, 'post': post, 'kategory': kategory,'insta':insta,'insta2':insta2,})

def post_list_view(request, kategory_slug=None):
    kategories = Kategory.objects.all()
    post = Post.objects.filter(status='published')
    if kategory_slug:
        kategory = get_object_or_404(Kategory, slug=kategory_slug)
        post = post.filter(kategory=kategory)
    list_objects = Post.published.all()
    paginator = Paginator(list_objects,1)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    products = Product.objects.filter(available=True)[0:3]
    insta = InstaRecap.objects.all()[0:5]
    recent = Post.objects.order_by('-publish')[0:5]
    kategorypostdictionary = {kategory: list(set([Post.objects.get( id=x ) for x in kategory.post_ids if len(kategory.post_ids) > 1])) for kategory in kategories}

    twoperkategory = {x: sample( kategorypostdictionary[x], 2 ) for x in kategorypostdictionary if len(list(set( kategorypostdictionary[x]))) > 1}
    return render(request, 'blog/post/list.html', {'posts': posts, 'products': products, 'insta':insta,'twoperkategory': twoperkategory,'recent': recent, })

def post_detail_view(request, year, month, day, post):
    recent = Post.objects.order_by('-publish')[0:3]
    kategories = Kategory.objects.all()
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'recent': recent,'kategories': kategories,
    'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    categorypic = Product.objects.filter(available=True)[0:1]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        categorypics = Product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'categorypics': categorypic
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    similar = Product.objects.filter(available=True)[0:5]
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'similar': similar,
    }
    return render(request, 'shop/product/detail.html', context)

def insta_recap(request):
    insta = InstaRecap.objects.all()
    return render(request, 'instaRecap.html', {'insta':insta})