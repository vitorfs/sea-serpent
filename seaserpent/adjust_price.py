import datetime
from unipath import Path
import sys
import os

PROJECT_DIR = Path(__file__).parent.parent
sys.path.append(PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seaserpent.settings')

import django
django.setup()

from seaserpent.core.models import Product, Company, ProductPriceHistory


products = ProductPriceHistory.objects.all()

for product in products:
    str_price = ''
    try:
        str_price = '{:.2f}'.format(product.price)
    except:
        str_price = '0'
    product.price = float(str_price)
    print product.price
    product.save()