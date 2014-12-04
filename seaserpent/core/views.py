from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from seaserpent.core.models import Product

def home(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if not order: order = ''
    if order.replace('-', '') not in ('product_key', 'name', 'price', 'updated_at', 'visited_at', 'status', 'price_difference', ):
        order = '-updated_at'
    products = Product.objects.exclude(status='novo').exclude(Q(price__isnull=True) | Q(price=0.0))
    if search:
        products = products.filter(name__icontains=search)
    products = products.order_by(order)
    paginator = Paginator(products, 100)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'core/home.html', { 'products': products, 'order': order, 'search': search })
    

def price_history(request, company, product_key):
    product = get_object_or_404(Product, product_key=product_key, company__name=company)
    return render(request, 'core/price_history.html', { 'product': product })