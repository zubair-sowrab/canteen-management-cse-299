
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm,MySetPasswordForm,MyPasswordResetForm,MyPasswordChangeForm
from django.contrib import admin


urlpatterns = [
    path("",views.home),
    path("about/",views.about,name="about"),
    path("feedback/",views.feedback,name="feedback"),
    path("paymentgateway/",views.payg,name="payment-gateway"),
   
    path('feedback/submit', views.feedback_submit, name='feedback_submit'),
    path('thank_you/', views.thank_you, name='thank_you'),

    path("contact",views.contact,name="contact"),
    path("category/<slug:values>",views.CategoryView.as_view(),name="category"),
    path("category-title/<values>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-details/<int:pks1>",views.ProductDetail.as_view(),name="product-details"),
    path("registration/",views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path("accounts/login/",auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path("password-reset/",auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("address/",views.ProfileView.as_view(),name="address"),
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('cart/checkout/',views.checkout.as_view(),name='checkout'),
    

    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',
    form_class=MyPasswordResetForm),name='password_reset'), 
  
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',
    form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html')
    ,name='passwordchangedone'), 

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html')
    ,name='password_reset_done'),

    


    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view (template_name='app/password_reset_confirm.html',
    form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html') ,
    name='password_reset_complete'),

   
    path('search/',views.search,name='search'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header="Daowat Admin Panel"
admin.site.site_title="Daowat"
admin.site.site_index_title="Welcome to Daowat"