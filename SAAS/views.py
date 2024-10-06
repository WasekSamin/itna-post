from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Package, PackageCheckout, Shop, Currency
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from restaurant.models import Employee
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import os, uuid
from django.core.mail import EmailMessage
import uuid
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator



# Create your views here.

# landing

def saasHome(request):
    packages = Package.objects.all()[:3]

    args = {
        "packages": packages,
    }
    return render(request, "landing/landing.html", args)

@login_required(login_url='/login/')
def packageDetails(request, id):
    package_obj = get_object_or_404(Package, id=id)
    all_currency = Currency.objects.all()

    # print("User:", request.user)

    package_checkout_obj = PackageCheckout.objects.filter(customer_obj=request.user)

    # print("PACKAGE CHECKOUT:", package_checkout_obj)
    if package_checkout_obj.exists():
        package_checkout_obj = package_checkout_obj.last()
        return redirect(f"/user-package/{package_checkout_obj.id}")

    args = {
        "package_obj": package_obj,
        "all_currency": all_currency,
    }
    return render(request, "package/packageDetails.html", args)

@login_required(login_url='/login/')
def packageCheckout(request, id):
    package_obj = get_object_or_404(Package, id=id)

    if request.method == "POST":
        customer_name = request.POST.get("cust_name")
        customer_contact = request.POST.get("cust_contact")
        shop_name = request.POST.get("shop_name")
        shop_logo_img = request.FILES.get("shop_logo")
        bkash_number = request.POST.get("user_bkash_number")
        bkash_trx = request.POST.get("user_bkash_trans_id")
        nagad_number = request.POST.get("user_nagad_number")
        nagad_trx = request.POST.get("user_nagad_trans_id")
        currency = request.POST.get("currency")

        # print(shop_name)

        shop_obj = Shop.objects.filter(shop_name=shop_name)
        shop_obj_user = Shop.objects.filter(user=request.user)
        print(shop_obj)
        user_exist = PackageCheckout.objects.filter(customer_obj=request.user)

        if shop_obj.exists():
            messages.error(request, "Shop with this name already exists!")
            return redirect(f"/package-details/{id}/")
        elif shop_obj_user.exists():
            messages.error(request, "User already has a shop!")
            return redirect(f"/package-details/{id}/")

        if user_exist.exists():
            messages.error(request, "Email is already being used! Please create a new account...")
            return redirect(f"/package-details/{id}/")

        if package_obj and customer_name and customer_contact and shop_name and shop_logo_img:
            if len(bkash_number) <= 0 and len(nagad_number) <= 0:
                messages.error(request, "You have to pay via bKash or Nagad!")
                return redirect(f"/package-details/{id}/")
            else:
                # For bKash
                if len(bkash_number) > 0:
                    if len(bkash_trx) > 0:
                        currency = get_object_or_404(Currency, currency_icon=currency)
                        shop_obj = Shop(
                            user=request.user,
                            shop_name=shop_name, 
                            shop_contact=customer_contact, 
                            shop_logo=shop_logo_img,
                            currency=currency,
                        )
                        shop_obj.save()

                        package_checkout_obj = PackageCheckout(
                            customer_obj=request.user,
                            customer_name=customer_name,
                            customer_phone_number=customer_contact,
                            shop=shop_obj,
                            package=package_obj,
                            total=package_obj.package_price,
                            bkash_number=bkash_number,
                            bkash_transaction_id=bkash_trx
                        )
                        package_checkout_obj.save()

                        # Pakcage due date
                        package_checkout_obj.due_date = package_checkout_obj.created_at + timedelta(days=package_obj.duration + 1)
                        package_checkout_obj.save()
                        
                        
                        # sending confirmation email to the buyer
                        rec = request.user.email
                        email_subject = "Your order has been placed"
                        email_message = render_to_string('mailView/purchase-mail-template.html', {})
                        email = EmailMultiAlternatives(email_subject, email_message, to=[rec])
                        email.attach_alternative(email_message, "text/html")
                        email.send()
                
                        return redirect("saas_success")
                    else:
                       messages.error(request, "Please submit bKash transaction ID!")
                       return redirect(f"/package-details/{id}/")
                # For nagad
                elif len(nagad_number) > 0:
                    if len(nagad_trx) > 0:
                        currency = get_object_or_404(Currency, currency_icon=currency)
                        shop_obj = Shop(user=request.user, shop_name=shop_name, shop_contact=customer_contact, shop_logo=shop_logo_img, currency=currency)
                        shop_obj.save()

                        package_checkout_obj = PackageCheckout(
                            customer_obj=request.user,
                            customer_name=customer_name,
                            customer_phone_number=customer_contact,
                            shop=shop_obj,
                            package=package_obj,
                            total=package_obj.package_price,
                            nagad_number=nagad_number,
                            nagad_transaction_id=nagad_trx
                        )
                        # Pakcage due date
                        package_checkout_obj.due_date = package_checkout_obj.created_at + timedelta(days=package_obj.duration + 1)
                        package_checkout_obj.save()

                        return redirect("saas_success")
                    else:
                        messages.error(request, "Please submit Nagad transaction ID!")
                        return redirect(f"/package-details/{id}/")
        else:
            messages.error(request, "Some fields are not fulfilled properly!")
            return redirect(f"/package-details/{id}/")

@login_required(login_url='/login/')
def userPackageView(request, id):
    package_checkout_obj = get_object_or_404(PackageCheckout, id=id)

    today_date = datetime.now() - timedelta(days=1)
    today_date = datetime.strftime(today_date, "%Y-%m-%d %H:%M:%S")
    today_date = datetime.strptime(today_date, "%Y-%m-%d %H:%M:%S")

    package_expired_date = package_checkout_obj.due_date
    package_expired_date = datetime.strftime(package_expired_date, "%Y-%m-%d %H:%M:%S")
    package_expired_date = datetime.strptime(package_expired_date, "%Y-%m-%d %H:%M:%S")

    # print(today_date)
    # print(package_expired_date)

    if today_date > package_expired_date:
        package_checkout_obj.is_expired = True
        package_shop = package_checkout_obj.shop

        shop_obj = get_object_or_404(Shop, id=package_shop.id)

        shop_obj.is_active = False

        package_checkout_obj.save()
        shop_obj.save()

    args = {
        "package_checkout_obj": package_checkout_obj,
    }
    return render(request, "package/userPackage.html", args)

# log in and registration
def logInView(request):
    packages = Package.objects.all()[:3]
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("landing")

    args = {
        "packages": packages,
    }
    return render(request, "account/login.html", args)


def regView(request):
    packages = Package.objects.all()[:3]
    message = None
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        # password2 = post_data.get("password2")

        user_exists = User.objects.filter(username=username)

        if user_exists.exists():
            messages.error(request, "The username already exists!")
            return redirect("registration")
      
        if len(password) >= 8:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False,
            )
            current_site = get_current_site(request)
            mail_subject = "Verify your account"
            message = render_to_string("account/verify.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
            send_mail = email
            email = EmailMultiAlternatives(mail_subject, message, to=[send_mail])
            email.attach_alternative(message, "text/html")
            email.send()

            messages.success(request, "Email Sent Please verify your account")
            messages.info(request, "Please Activate Your Account ASAP")
            return redirect("login")
        else:
            message = "Password is too short. It must contain 8 characters"
    args = {
        "packages": packages,
        "message": message
    }
    return render(request, "account/registration.html", args)




UserModel = get_user_model()
def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        # user = UserModel._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is now activated or verified")
        return redirect("login")
    else:
        # messages.warning(request, "Invalid Activaton Link Please Try again later")
        # return redirect("user_registration")
        return HttpResponse("Activation Link is invalid")



# Logout View Function

def logout_user(request):
    logout(request)
    return redirect("login")

# footer pages    
# about us
def aboutusView(request):
    args = {}
    return render(request, "footer_pages/aboutus.html", args)  

# support
def supportView(request):
    args = {}
    return render(request, "footer_pages/support.html", args) 

# Success-Error Page
def successPageView(request):
    return render(request, "saas_except/success.html")

def failedPageView(request):
    return render(request, "saas_except/failed.html")