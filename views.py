from django.db.models import Count,Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from . models import Product,Customer,Cart
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.
@login_required 
def home(request):
    totalitem=0
    if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))   
    return render(request,"app/home.html",locals())

@login_required 
def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html")

@login_required 
def contact(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html")

@login_required     
def feedback(request):
    return render(request,"app/feedback.html")

@login_required 
def payg(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/paymentgateway.html")


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,values):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        product=Product.objects.filter(category=values)
        title=Product.objects.filter(category=values).values('title').annotate(total=Count('title'))
        return render(request,"app/category.html",locals())


@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,values):
        product=Product.objects.filter(title=values)
        title=Product.objects.filter(category=product[0].category).values('title')
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())
    

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pks1):
        product=Product.objects.get(pk=pks1)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
       
        return render(request,"app/productdetail.html",locals())    
    



class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
       
        return render(request,"app/customerregistration.html",locals())
   
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! Registration Successful.")
        else:
            messages.warning(request,"Invalid Inputs")
        return render(request,"app/customerregistration.html",locals())


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,"app/profile.html",locals())


    def post(self,request):
        form=CustomerProfileForm(request.POST)
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
       
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            nsu_id=form.cleaned_data['nsu_id']
            nsu_mail=form.cleaned_data['nsu_mail']
            mobile=form.cleaned_data['mobile']

            reg=Customer(user=user,name=name,nsu_id=nsu_id,nsu_mail=nsu_mail,mobile=mobile)
            reg.save()
            messages.success(request,"Congratulations! Your details have been saved successfully!")
        else:
            messages.warning(request,"Data Entered Is Invalid!!!")
        return render(request,"app/profile.html",locals())


@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount=amount+value    
    totalamount=amount
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
       
    return render(request,'app/addtocart.html',locals())

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
       
        user=request.user
        customer=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
       
        famount=0
        for p in cart_items:
            value=p.quantity*p.product.discounted_price
            famount=famount+value
        totalamount=famount
        return render(request,'app/checkout.html',locals())


    



def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
        totalamount=amount
        data={'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)




def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount-value
        totalamount=amount
        data={'quantity':c.quantity,
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)



def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discounted_price
            amount=amount+value
        totalamount=amount
        data={
                'amount':amount,
                'totalamount':totalamount
        }
        return JsonResponse(data)






@login_required
def feedback(request):
    if request.method == 'POST':
        satisfaction = request.POST.get('satisfaction')
        comment = request.POST.get('comment')
        user = request.user

        feedback = Feedback.objects.create(
            user=user,
            satisfaction=satisfaction,
            comment=comment
        )

        # Optionally, you can perform additional actions here,
        # such as sending notifications or redirecting the user.

        return redirect('home')  # Replace 'home' with the desired URL

    return render(request, "app/feedback.html")



@login_required
def feedback_submit(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback')
        feedback = Feedback(rating=rating, text=feedback_text)
        feedback.save()
        return redirect('thank_you')  # Assuming you have a 'thank_you' URL pattern

    return render(request, 'app/feedback.html')




def thank_you(request):
    return render(request, 'app/thank_you.html')


@login_required
def search(request):
    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html",locals())