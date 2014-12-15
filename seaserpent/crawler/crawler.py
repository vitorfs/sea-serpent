import urllib2
import datetime
from seaserpent.core.models import Product, Company, ProductPriceHistory

class SeaSerpent(object):
    product_list = []
    visited_products = []
    links = []
    visited_links = []
    company = None
    base_url = ''

    def __init__(self, name):
        self.company = Company.objects.get(name=name)
        self.base_url = self.company.url

    def _do_request(self, url):
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
            return response
        except Exception, e:
            with open('error.log', 'a') as f:
                f.write(u'Exception: {0}\nUrl: {1}\n\n'.format(e, url))
            raise e

    def _request(self, url):
        response = self._do_request(url)
        return response.readlines()

    def _remove_visited_links(self):
        self.links = list(set(self.links))
        temp_list = []
        for link in self.links:
            if link not in self.visited_links:
                temp_list.append(link)
        self.links = temp_list

    def _catalog_products(self, products):
        for product_key in products:
            if not Product.objects.filter(product_key=product_key, company=self.company):
                Product(product_key=product_key, company=self.company).save()

    def discover(self, url):
        return

    def discover_products(self):
        self.links.append(self.base_url)
        while self.links:
            link = self.links.pop()
            self.discover(link)

    def _save_product(self, product, name, price, em_estoque):
        product.visited_at = datetime.datetime.now()
        try:
            if name != '':
                product.name = name.strip()
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
                    if product.price != price:
                        product.status = 'ok'
                        product.last_price = product.price
                        product.price = price
                        product.price_difference = product.price - product.last_price
                        product.updated_at = datetime.datetime.now()
                        ProductPriceHistory(product=product, price=price).save()
                        product.price_changes = product.price_changes + 1

                        if product.price != None and product.last_price != None and product.price != 0 and product.last_price != 0:
                            if product.last_price < product.price:
                                product.price_percentage_change = product.last_price / product.price
                                product.price_percentage_change = 1.0 - product.price_percentage_change
                            elif product.last_price > product.price:
                                product.price_percentage_change = product.price / product.last_price
                                product.price_percentage_change = product.price_percentage_change - 1.0
                            else:
                                product.price_percentage_change = 0.0
                        else:
                            product.price_percentage_change = 0.0
                            
                else:
                    product.status = 'esgotado'
            else:
                product.status = 'nao_encontrado'
        except Exception, e:
            product.status = 'erro'
        product.save()

    def lunge(self, product):
        return

    def collect_data(self, number = 0, total = 1):
        while True:
            products = Product.objects.filter(company=self.company).order_by('-visited_at')
            for product in products:
                if product.id % total == number: # multi thread varrendo um lote de produtos
                    self.lunge(product)
                    try:
                        self.discover('{0}/produto/{1}'.format(self.base_url, product.product_key))
                        self.visited_links = []
                    except Exception, e:
                        pass


class SubmarinoSerpent(SeaSerpent):

    def __init__(self):
        SeaSerpent.__init__(self, 'submarino')

    def discover(self, url):
        self.visited_links.append(url)
        products = []
        try:
            html = self._request(url)
            for line in html:
                if ' href="http://www.submarino.com.br/' in line:
                    splited_line = line.split(' href="')
                    link = splited_line[1].partition('"')[0]
                    self.links.append(link)
                if ' href="http://www.submarino.com.br/produto/' in line:
                    splited_line = line.split(' href="http://www.submarino.com.br/produto/')
                    product = splited_line[1].partition("/")[0].partition("?")[0]
                    products.append(product)
            self._remove_visited_links()
            self._catalog_products(products)
        except Exception, e:
            pass

    def lunge(self, product):
        name = ''
        price = ''
        em_estoque = True
        try:
            url = '{0}/produto/{1}'.format(self.base_url, product.product_key)
            html = self._request(url)
            for line in html:
                if ' data-partner-value' in line:
                    splited_line = line.split(' data-partner-value="') 
                    price = splited_line[1].partition('"')[0]
                if 'mp-tit-name' in line:
                    splited_line = line.split(' title="')
                    name = splited_line[1].partition('"')[0]
                if 'unavailable-product' in line:
                    em_estoque = False
            self._save_product(product, name, price, em_estoque)
        except Exception, e:
            pass


class AmericanasSerpent(SeaSerpent):

    def __init__(self):
        SeaSerpent.__init__(self, 'americanas')

    def discover(self, url):
        self.visited_links.append(url)
        products = []
        try:
            html = self._request(url)
            for line in html:
                if ' href="http://www.americanas.com.br/' in line:
                    splited_line = line.split(' href="')
                    link = splited_line[1].partition('"')[0]
                    self.links.append(link)
                if ' href="http://www.americanas.com.br/produto/' in line:
                    splited_line = line.split(' href="http://www.americanas.com.br/produto/')
                    product = splited_line[1].partition("/")[0].partition("?")[0]
                    products.append(product)
            self._remove_visited_links()
            self._catalog_products(products)
        except Exception, e:
            pass

    def lunge(self, product):
        name = ''
        price = ''
        em_estoque = True
        try:
            url = '{0}/produto/{1}'.format(self.base_url, product.product_key)
            html = self._request(url)
            for line in html:
                if ' data-price' in line:
                    splited_line = line.split(' data-price="') 
                    price = splited_line[1].partition('"')[0]
                if 'mp-tit-name' in line:
                    splited_line = line.split(' title="')
                    name = splited_line[1].partition('"')[0]
                if 'unavailable-product' in line:
                    em_estoque = False
            self._save_product(product, name, price, em_estoque)
        except Exception, e:
            pass


class ShoptimeSerpent(SeaSerpent):

    def __init__(self):
        SeaSerpent.__init__(self, 'shoptime')

    def discover(self, url):
        self.visited_links.append(url)
        products = []
        try:
            html = self._request(url)
            for line in html:
                if ' href="http://www.shoptime.com.br/' in line:
                    splited_line = line.split(' href="')
                    link = splited_line[1].partition('"')[0]
                    self.links.append(link)
                if ' href="http://www.shoptime.com.br/produto/' in line:
                    splited_line = line.split(' href="http://www.shoptime.com.br/produto/')
                    product = splited_line[1].partition("/")[0].partition("?")[0]
                    products.append(product)
            self._remove_visited_links()
            self._catalog_products(products)
        except Exception, e:
            pass

    def lunge(self, product):
        name = ''
        price = ''
        em_estoque = True
        try:
            url = '{0}/produto/{1}'.format(self.base_url, product.product_key)
            html = self._request(url)
            
            price_buffer = ''
            read_price = False

            title_buffer = ''
            read_title = False

            for line in html:

                if read_title:
                    title_buffer = title_buffer + line
                    if '</div>' in line:
                        read_title = False

                if read_price:
                    price_buffer = price_buffer + line
                    if '<span class="ct">' in line:
                        read_price = False

                if 'pricingInfo"' in line:
                    read_price = True
                if '<div class="prodTitle">' in line:
                    read_title = True
                if 'unavailProd' in line:
                    em_estoque = False

            if title_buffer:
                try:
                    title_buffer = title_buffer.replace('<h1 class="title">', '')
                    title_buffer = title_buffer.replace('</h1>', '')
                    title_buffer = title_buffer.replace('</div>', '')
                    name = title_buffer.strip()
                except Exception, e:
                    name = ''

            if price_buffer:
                try:
                    price_buffer = price_buffer.split('sale price')[1].partition('<span class="discount">')[0]
                    price_buffer = ''.join(c for c in price_buffer if c.isdigit())
                    price = float(price_buffer[:len(price_buffer) - 2] + '.' + price_buffer[-2:])
                except Exception, e:
                    price = 0.0
            self._save_product(product, name, price, em_estoque)
        except Exception, e:
            pass
