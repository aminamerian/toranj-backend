from django.db import models
from django.utils.crypto import get_random_string


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    # Indicating whether the category is leaf or not
    is_leaf = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    uid = models.CharField(max_length=12, unique=True, editable=False)
    page_url = models.URLField(max_length=250, unique=True)
    shop = models.ForeignKey('Shop', on_delete=models.RESTRICT, related_name='products')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.RESTRICT, related_name='products')
    name = models.CharField(verbose_name='عنوان', max_length=150)
    price = models.IntegerField(verbose_name='مبلغ', null=False, blank=False, db_index=True)
    is_available = models.BooleanField()
    features = models.CharField(max_length=250, blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Provide a random 12 length string for uid.
        if not self.uid:
            self.uid = get_random_string(12)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.shop}'


class Shop(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام فروشگاه', null=False, blank=False)
    domain = models.URLField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class PriceChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_change_logs')
    price = models.IntegerField(null=False, blank=False)
    is_available = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
