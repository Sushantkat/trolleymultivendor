from email.policy import default
from django.db import models
from product.models import Product
from vendor.models import Vendor
from accounts.models import MyUser

# Create your models here.
PAYMENT_CHOICES = [
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
]


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    vendors = models.ManyToManyField(MyUser, related_name="orders")
    customers = models.ForeignKey(
        MyUser, related_name="orderss", on_delete=models.CASCADE
    )
    payment = models.CharField(max_length=30, choices=PAYMENT_CHOICES)
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    vendor = models.ForeignKey(MyUser, related_name="items", on_delete=models.CASCADE)
    customer = models.ForeignKey(MyUser, related_name="item", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.order)

    def get_total_price(self):
        return self.price * self.quantity


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
