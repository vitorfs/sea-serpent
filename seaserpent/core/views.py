from django.shortcuts import render, get_object_or_404
from seaserpent.core.models import Product

def home(request):
    products = Product.objects.exclude(status='novo').order_by('-updated_at')
    return render(request, 'core/home.html', { 'products' : products })

def price_history(request, product_key):
    product = get_object_or_404(Product, product_key=product_key)
    return render(request, 'core/price_history.html', { 'product' : product })