from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES=(
    ('BR','Breakfast'),
    ('LU','Lunch'),
    ('DI','Dinner'),
    ('SN','Snacks'),
    ('BE','Beverages'),
    
)


STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Cancel','Cancel'),
    ('Preparing','Preparing'),
    ('Ready','Ready'),
   
    
)




# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=100)
    sellingprice=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='products')
    def _str_(self):
        return self.title
    
    
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    nsu_id=models.IntegerField(default=0)
    nsu_mail=models.CharField(max_length=200)
    mobile=models.IntegerField(default=0)
    def _str_(self):
        return self.name





class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    @property
    def total_cost(self):
       return self.quantity*self.product.discounted_price


class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    bkash_order_id=models.CharField(max_length=100,blank=True,null=True)
    bkash_payment_status=models.CharField(max_length=100,blank=True,null=True)
    bkash_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=True)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    


class Feedback(models.Model):
    rating = models.CharField(max_length=20)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    satisfaction = models.CharField(choices=(
        ('Unhappy', 'Unhappy'),
        ('Neutral', 'Neutral'),
        ('Satisfied', 'Satisfied'),
    ), max_length=10)
    comment = models.TextField()

    def __str__(self):
        return f"Feedback from {self.user.username}"
