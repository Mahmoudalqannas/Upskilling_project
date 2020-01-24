from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('L', 'Laptops'),
    ('SM', 'Smart phones'),
    ('T', 'Tablets')
)

CITY_CHOICES = (
    ('Amman', 'Amman'),
    ('Irbid', 'Irbid'),
    ('Zarqaa', 'Zarqaa'),
    ('Aqaba', 'Aqaba'),
    ('Alkarak', 'Alkarak'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class CategoryProduct(models.Model):

    category_product = models.CharField(choices=CATEGORY_CHOICES, max_length=2)

    def __str__(self):
        return self.category_product


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey(
        to='CategoryProduct', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    image_tow = models.ImageField(blank=True, null=True)
    image_three = models.ImageField(blank=True, null=True)
    image_four = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class ProductTags(models.Model):
    tag_name = models.ManyToManyField(to='Tag')
    tag_product = models.OneToOneField(
        to='Item', on_delete=models.CASCADE, null=True, blank=True, unique=True)

    # def __str__(self):
    #     return self.tag_name


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(choices=CITY_CHOICES, max_length=10)
    phone_number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.username
