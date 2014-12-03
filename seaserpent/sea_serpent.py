import urllib2
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

class SeaSerpent:
    base_url = 'http://submarino.com.br'
    product_list = []
    visited_products = []
    links = []
    visited_links = []
    company = Company.objects.get(name='submarino')

    def _request(self, url):
        try:
            header = { 
                'User-Agent': 'SeaSerpent/0.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Connection': 'keep-alive'
                }
            req = urllib2.Request(url, headers=header)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception, e:
            with open('log.txt', 'a') as f:
                f.write(u'Exception: {0}\nUrl: {1}\n\n'.format(e, url))
            raise e

    def discover(self, url):
        self.visited_links.append(url)
        products = []
        try:
            html = self._request(url)
            lines = html.split('\n')
            for line in lines:
                if ' href="http://www.submarino.com.br/' in line:
                    splited_line = line.split(' href="')
                    link = splited_line[1].partition('"')[0]
                    self.links.append(link)
                if ' href="http://www.submarino.com.br/produto/' in line:
                    splited_line = line.split(' href="http://www.submarino.com.br/produto/')
                    product = splited_line[1].partition("/")[0].partition("?")[0]
                    products.append(product)

            self.links = list(set(self.links))
            temp_list = []
            for link in self.links:
                if link not in self.visited_links:
                    temp_list.append(link)
            self.links = temp_list

            for product_key in products:
                if not Product.objects.filter(product_key=product_key):
                    Product(product_key=product_key, company=self.company).save()
        except Exception, e:
            print e
            pass

    def lunge(self, product):
        url = '{0}/produto/{1}'.format(self.base_url, product.product_key)

        try:
            html = self._request(url)
            lines = html.split('\n')
            name = ''
            price = ''
            em_estoque = True

            for line in lines:
                if ' data-partner-value' in line:
                    splited_line = line.split(' data-partner-value="') 
                    price = splited_line[1].partition('"')[0]
                if 'mp-tit-name' in line:
                    splited_line = line.split(' title="')
                    name = splited_line[1].partition('"')[0]
                if 'unavailable-product' in line:
                    em_estoque = False

            print product.product_key + ' ' + name + ' ' + price

            product.visited_at = datetime.datetime.now()

            if name != '':
                product.name = name
                if em_estoque:
                    try:
                        price = round(float(price), 2)
                    except Exception, e:
                        price = 0.0

                    if product.status == 'novo':
                        product.price = price
                        product.status = 'ok'
                        product.updated_at = datetime.datetime.now()
                        ProductPriceHistory(product=product, price=price).save()

                    if str(product.price) != str(price):
                        product.price = price
                        product.updated_at = datetime.datetime.now()
                        ProductPriceHistory(product=product, price=price).save()
                else:
                    product.status = 'esgotado'
            else:
                product.status = 'nao_encontrado'
            
        except Exception, e:
            print e
            product.status = 'nao_encontrado'
            product.updated_at = datetime.datetime.now()
            product.visited_at = datetime.datetime.now()

        product.save()

    def collect_products(self):
        products = Product.objects.filter(status='novo')
        for product in products:
            self.lunge(product)

    def discover_products(self):
        self.links.append(self.base_url)
        while self.links:
            link = self.links.pop()
            self.discover(link)
