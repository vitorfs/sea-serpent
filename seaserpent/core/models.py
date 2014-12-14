from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_key = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    last_price = models.FloatField(null=True)
    price_difference = models.FloatField(null=True)
    company = models.ForeignKey(Company)
    status = models.CharField(max_length=20, default='novo')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    visited_at = models.DateTimeField(auto_now_add=True)
    price_changes = models.IntegerField(default=0)
    price_percentage_change = models.FloatField(default=0.0)

    def _format(self, price):
        formatted_price = u''
        if self.price:
            try:
                formatted_price = u'R$ {:.2f}'.format(price)
            except:
                pass
        return formatted_price

    def display_price(self):
        return self._format(self.price)

    def display_price_difference(self):
        return self._format(self.price_difference)

    def display_price_percentage_change(self):
        value = self.price_percentage_change * 100
        return u'{:.2f}%'.format(value)

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
