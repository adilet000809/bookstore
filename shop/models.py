# Importing required libraries
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# Database models


# A Category table is database
class Category(models.Model):
    # Fields of Category table
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    # Representation of Category item in Django Admin Panel
    def __str__(self):
        return self.name

    # Absolute url for category item
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.slug)])


# A manager to filter products
class ProductManager(models.Manager):
    def all(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


# A Product table in database
class Product(models.Model):
    # Fields of Product table
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='book_image')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = ProductManager()

    # Representation of Product item in Djaango Admin Panel
    def __str__(self):
        return self.title

    # Absolute url for Product item
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.slug)])


# A CartItem table in database
class CartItem(models.Model):
    # Fields of CartItem table
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True)

    # Representation of CartItem item in Django Admin Panel
    def __str__(self):
        return "Cart item for product {0}".format(self.product.title)

    # A function to retrieve price for certain CartItem item
    def cart_item_price(self):
        return self.quantity*self.product.price


# A Cart table in database
class Cart(models.Model):
    # Fields of Cart table
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=False)
    order_date = models.DateTimeField(auto_now=True)

    # Representation of Cart item in Django Admin Panel
    def __str__(self):
        return str(self.id)

    # A function to retrieve Cart item from table
    def get_cart_items(self):
        return self.cartitem_set.all()

    # A function to retrieve number of Cart items
    def get_cart_items_count(self):
        return self.cartitem_set.all().count()

    # A function to retrieve total price of Cart items
    def get_cart_total(self):
        return sum([item.product.price*item.quantity for item in self.get_cart_items()])


# Tuple of Order statuses
ORDER_STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Waiting for the recipient', 'Waiting for the recipient'),
    ('Handed over', 'Handed over')
)

# Tuple of choices to obtain the order
BUY_TYPE_CHOICES = (
    ('Pickup', 'Pickup'),
    ('Delivery', 'Delivery')
)


# A Order table of database
class Order(models.Model):
    # Fields of Order table
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    items = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255, null=True, blank=True)
    buy_type = models.CharField(max_length=30, choices=BUY_TYPE_CHOICES, default='Pickup')
    comments = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Accepted')
    date = models.DateField(auto_now=True)

    # Absolute url for certain Order item
    def get_absolute_url(self):
        return reverse('order_detail', args=[self.id])

    # Representation of Order items in Django Admin Panel
    def __str__(self):
        return 'Order #{order}'.format(order=str(self.id))


# A ShopManager table in database
class ShopManager(models.Model):
    # Fields of manager table
    user = models.OneToOneField(User, related_name='manager', on_delete=models.CASCADE)
    role = 'manager'

    # Representation of ShopManager items in Django Admin Panel
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

