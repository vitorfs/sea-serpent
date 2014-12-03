from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_key = models.CharField(max_length=255, unique=True)
    price = models.FloatField(null=True)
    company = models.ForeignKey(Company)
    status = models.CharField(max_length=20, default='novo')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    def display_price(self):
        formatted_price = u''
        if self.price:
            try:
                formatted_price = u'R$ {:.2f}'.format(self.price)
            except:
                pass
        return formatted_price

    def get_last_price(self):
        history = ProductPriceHistory.objects.filter(product=self).exclude(price=self.price).order_by('-date')
        diff = 0.0
        if history:
            last_price = history[0].price
            diff = self.price - last_price
        return diff

    def get_history(self):
        history = ProductPriceHistory.objects.filter(product=self).order_by('-date')
        return history

class ProductPriceHistory(models.Model):
    product = models.ForeignKey(Product)
    price = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def display_price(self):
        try:
            return u'R$ {:.2f}'.format(self.price)
        except Exception, e:
            return u''
