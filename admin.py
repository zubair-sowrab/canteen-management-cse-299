from django.contrib import admin
from . models import Product,Customer,Cart
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discounted_price','category','product_image']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','nsu_id','nsu_mail','mobile']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
   list_display=['id','user','products','quantity']
   def products(self,obj):
    link=reverse("admin:app_product_change",args=[obj.product.pk])
    return format_html('<a href="{}">{}</a>',link,obj.product.title)

#@admin.register(Payment)
#class PaymentModelAdmin(admin.ModelAdmin):
 #  list_display=['id','user','amount','bkash_order_id','bkash_payment_status','bkash_payment_id','paid']