from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from seaserpent.core.models import Product, ProductPriceHistory
import datetime
def home(request):

    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)

    positive_changes_today = Product.objects.filter(updated_at__gt=today).exclude(Q(price__isnull=True) | Q(price=0.0)).order_by('price_percentage_change')[:10]
    negative_changes_today = Product.objects.filter(updated_at__gt=today).exclude(Q(price__isnull=True) | Q(price=0.0)).order_by('-price_percentage_change')[:10]

    search = request.GET.get('search')
    order = request.GET.get('order')
    if not order: order = ''
    if order.replace('-', '') not in ('product_key', 'name', 'price', 'updated_at', 'visited_at', 'status', 'price_difference', 'price_changes', 'price_percentage_change'):
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
    return render(request, 'core/home.html', { 'products': products, 
        'order': order, 
        'search': search,
        'positive_changes_today': positive_changes_today,
        'negative_changes_today': negative_changes_today
        })
    

def price_history(request, company, product_key):
    product = get_object_or_404(Product, product_key=product_key, company__name=company)
    chart_data = ProductPriceHistory.objects.filter(product=product).order_by('date')
    return render(request, 'core/price_history.html', { 'product': product, 'chart_data': chart_data })