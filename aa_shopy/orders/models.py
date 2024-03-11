from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserAddress
from django.utils import timezone
from store.models import ProductVariant
from datetime import timedelta


# Create your models here.


class Order(models.Model):
    PAYMENT_STATUS_CHOICE = [
        ('PENDING','Pending'),
        ('PAID','Paid'),
        ('CANCELLED','Cancelled'),
        ('DELIVERED','Delivered'),
        ('SHIPPED','shipped'),
        ('ORDERED','ordered'),
        ('RETURN','return'),
        ('REFUND','refund'),


        
    ]

    PAYMENT_METHOD_CHOICES=[
        ('PREPAID','PREPAID'),
        ('CASH_ON_DELIVERY','Cash on Delivery'),
        ('WALLET','wallet'),

    ]
    ORDER_STATUS_CHOICES = [
        ('CANCELLED', 'Cancelled'),
        ('DELIVERED', 'Delivered'),
        ('SHIPPED', 'Shipped'),
        ('RETURNED', 'Returned'),
        ('REQUESTED FOR RETURN','Requested for return'),
        ('ORDERED', 'Ordered'),
    ]


    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey('userprofile.UserAddress',on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Ordered', null=True, blank=True)
    shipping_date = models.DateTimeField(blank=True, null=True)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICE,default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    delivery_date=models.DateTimeField(blank=True,null=True)
    payment_id=models.CharField(blank=True,null=True)
    address_details = models.TextField(blank=True)
    razor_pay_payment_id = models.CharField(max_length=150, null=True, blank=True)
    razor_pay_order_id = models.CharField(max_length=150, null=True, blank=True)
    razor_pay_payment_signature =models.CharField(max_length=150, null=True, blank=True)
    return_period_expired=models.DateTimeField(blank=True, null=True)


    def _str_(self):
        return f"{self.id} {self.user.username}"

    def save(self,*args,**kwargs):
        if not self.order_date:
            self.order_date=timezone.now()

        if not self.delivery_date:
            self.delivery_date = self.order_date + timedelta(hours=24)
        super().save(*args,**kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.order.id}"


class Notifications(models.Model):
    order = models.ForeignKey(Order,  on_delete=models.CASCADE)
    action_required = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    comment = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
