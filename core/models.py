from django.db import models
from django.conf import settings

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL , on_delete=models.CASCADE
    )

    def __str__(self):
        return self.first_name

    # class Meta:
    #      ordering = ['first_name', 'last_name']        

class Category(models.Model):
    name = models.CharField(max_length=50)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='categorys', blank=True)

    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'price']        

class Game(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE , related_name="games")
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name="games")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name} - {self.product.title}'

class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE , related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name} - {self.balance}'

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE ,related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wallet.customer.first_name} {self.wallet.customer.last_name} - {self.amount}'


class Loan(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT , related_name="loans")

    