from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from seaserpent.core.models import Product

def home(request):
    order = request.GET.get('order')
    if not order: order = ''
    if order.replace('-', '') not in ('product_key', 'name', 'price', 'updated_at', 'visited_at', 'status', 'price_difference', ):
        order = '-updated_at'
    products = Product.objects.exclude(status='novo').exclude(price=0.0).order_by(order)
    paginator = Paginator(products, 100)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'core/home.html', { 'products': products, 'order': order })
    

def price_history(request, product_key):
    product = get_object_or_404(Product, product_key=product_key)
    return render(request, 'core/price_history.html', { 'product': product })