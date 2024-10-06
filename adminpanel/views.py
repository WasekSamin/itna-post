from functools import total_ordering
from django.db.models.fields import DecimalField
from django.http.response import Http404, HttpResponseGone
from django.shortcuts import get_object_or_404, render, redirect
from restaurant.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Sum, Avg
from django.contrib import messages
from .models import Contact
import csv
from datetime import date, datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
from TrashApp.models import *
from SAAS.models import PackageCheckout

import json


def login_for_admin(request):
    # shop_id = get_object_or_404(Shop, pk=shop_id)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        employee_obj = Employee.objects.filter(
            emp_username=username, emp_pin=password)

        if employee_obj.exists():
            employee_obj = employee_obj.last()
            request.session["employee_session"] = employee_obj.emp_username
            return redirect(f"/restaurant/start-selling-session/{employee_obj.shop.id}/")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_authenticated:
                # print(user.id)
                # print(user)
                shop_id = get_object_or_404(Shop, user=user)
                print(shop_id)
                login(request, user)
                return redirect(f"/adminpanel/home/{shop_id.id}/")
            else:
                messages.error(request, "Something went wrong!")
                return redirect(f"/adminpanel/login/")
        else:
            messages.error(request, "Invalid user credentials!")
            return redirect(f"/adminpanel/login/")
    args = {}
    return render(request, "account/admin_login.html", args)


def logoutView(request):
    # shop_id = get_object_or_404(Shop, pk=shop_id)
    emp_session = request.session.get("employee_session", None)
    if emp_session is not None:
        del request.session["employee_session"]
    logout(request)
    return redirect("login_for_admin")


# Package expired checking
def packageExpiredCheck(package_checkout_obj):
    # print(package_checkout_obj.shop)
    today_date = datetime.now() - timedelta(days=1)
    today_date = datetime.strftime(today_date, "%Y-%m-%d %H:%M:%S")
    today_date = datetime.strptime(today_date, "%Y-%m-%d %H:%M:%S")

    package_expired_date = package_checkout_obj.due_date
    package_expired_date = datetime.strftime(package_expired_date, "%Y-%m-%d %H:%M:%S")
    package_expired_date = datetime.strptime(package_expired_date, "%Y-%m-%d %H:%M:%S")

    if today_date > package_expired_date:
        package_checkout_obj.is_expired = True
        package_shop = package_checkout_obj.shop

        shop_obj = get_object_or_404(Shop, id=package_shop.id)

        shop_obj.is_active = False

        package_checkout_obj.save()
        shop_obj.save()
        return True
    return False


# @login_required(login_url="login_for_admin")
def adminpanelHome(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")


    emp_session = request.session.get("employee_session")
    print("SESSION:", emp_session)


    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
    print(emp_obj)

    # print("JOHNSON" + str(sellingsession.id))
    current_year = date.today().year
    year_type = request.GET.get("filtered_year")

    print("YEAR TYPE:", str(year_type))

    if year_type is not None and year_type != "all":
        current_year = year_type
    elif year_type is None or year_type == "all":
        current_year = date.today().year

    if (shop_id.user == request.user) or (emp_obj is not None and emp_obj.role.is_admin == True):
        customer_amount = Customer.objects.filter(
            shop=shop_id
        ).count()

        # shop_years = []

        # Shop.objects.filter(created_at)
        
        # Daily Sale
        
        today__date = date.today()
        daily__sale = RestCheckout.objects.filter(
                shop=shop_id, status="PAID", created_date=today__date
            ).aggregate(Sum("grand_total"))
        daily_sale = daily__sale.pop("grand_total__sum")
        
        # Gross Sales
        gs = RestCheckout.objects.filter(
            shop=shop_id, status="PAID"
        ).aggregate(Avg("grand_total"))
        gs_sale = gs.pop("grand_total__avg")
        # Total Transaction
        total_transaction = RestCheckout.objects.filter(
            shop=shop_id, status="PAID"
        ).aggregate(Sum("grand_total"))
        # delete_key = "grand_total"
        pipi = total_transaction.pop("grand_total__sum")
        print(pipi)
        # del total_transaction["grand_total__sum"]
        print(type(total_transaction))

        # Customer data for chart section starts
        total_customer_list = []
        customers = Customer.objects.filter(
            shop=shop_id, created_at__year=current_year)

        for cust in customers:
            # print(cust.created_at.month)
            total_customer_list.append(cust.created_at.month)

        total_customer_set = set(total_customer_list)
        # print(total_customer_set)

        customer_unqiue_month_count = []
        for item in total_customer_set:
            customer_unqiue_month_count.append(
                {str(item): total_customer_list.count(item)})

        del total_customer_list

        customer_unqiue_month_count = json.dumps(customer_unqiue_month_count)
        # Customer data for chart section ends

        # Total transaction data for chart section starts
        transactions = RestCheckout.objects.filter(
            shop=shop_id, status="PAID", created_at__year=current_year)
        print("Transactions", transactions)
        get_month_list = []

        for item in transactions:
            get_month_list.append({item.created_at.month: item.grand_total})

        print(get_month_list)
        del transactions

        transaction_unqiue_month_count = []
        all_months = list(range(1, 13))  # [1, 2, 3, 4, ...., 12]
        month_total_price = list(range(0, 12))
        month_total_price = list(
            map(lambda x: x*0, month_total_price))  # [0, 0, 0, ..., 0]
        print(month_total_price)

        for item in get_month_list:
            for k, v in item.items():
                if k == all_months[0]:
                    month_total_price[0] += v
                elif k == all_months[1]:
                    month_total_price[1] += v
                elif k == all_months[2]:
                    month_total_price[2] += v
                elif k == all_months[3]:
                    month_total_price[3] += v
                elif k == all_months[4]:
                    month_total_price[4] += v
                elif k == all_months[5]:
                    month_total_price[5] += v
                elif k == all_months[6]:
                    month_total_price[6] += v
                elif k == all_months[7]:
                    month_total_price[7] += v
                elif k == all_months[8]:
                    month_total_price[8] += v
                elif k == all_months[9]:
                    month_total_price[9] += v
                elif k == all_months[10]:
                    month_total_price[10] += v
                elif k == all_months[11]:
                    month_total_price[11] += v
                elif k == all_months[12]:
                    month_total_price[12] += v

        print(month_total_price)

        transaction_unqiue_month_count = json.dumps(
            month_total_price, cls=DjangoJSONEncoder)

        del month_total_price
        # Total transaction data for chart section ends

        # Filter year section starts
        customer_years = set()
        all_customers = Customer.objects.filter(shop=shop_id)

        for item in all_customers:
            customer_years.add(item.created_at.year)
        print(customer_years)

        transaction_years = set()
        all_transactions = RestCheckout.objects.filter(
            status="PAID", shop=shop_id)

        for item in all_transactions:
            transaction_years.add(item.created_at.year)
        print(transaction_years)

        filtering_years = set()

        if len(customer_years) > 0:
            for item in customer_years:
                filtering_years.add(item)
        if len(transaction_years) > 0:
            for item in transaction_years:
                filtering_years.add(item)

        del customer_years

        print("FILTERED YEARS:", filtering_years)
        # Filter year section ends

        args = {
            "shop_id": shop_id,
            "customer_amount": customer_amount,
            "total_transaction": total_transaction,
            "gs": gs,
            "pipi": pipi,
            "gs_sale": gs_sale,
            "current_year": current_year,
            "customer_unqiue_month_count": customer_unqiue_month_count,
            "transaction_unqiue_month_count": transaction_unqiue_month_count,
            "filtering_years": filtering_years,
            "year_type": year_type,
            "daily_sale": daily_sale,
        }
        return render(request, "adminpanel/admin-panel.html", args)
    else:
        return redirect("warning")


def adminShopLogoUpdate(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        shop_logo = request.FILES.get("shop_logo")

        shop_id.shop_logo = shop_logo
        shop_id.save()
        return redirect(f"/adminpanel/home/{shop_id.id}/")


# @login_required(login_url="login_for_admin")
def adminpanelOrder(request, shop_id):
    order_type = request.GET.get("order_type")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    print("ORDER TYPE:", order_type)
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_orders == True)):
        orders = RestCheckout.objects.filter(
            shop=shop_id
        )

        if request.method == "GET":
            order_type = request.GET.get("order_type")

            if order_type == "all":
                orders = RestCheckout.objects.filter(
                    shop=shop_id
                )
            elif order_type == "paid":
                orders = RestCheckout.objects.filter(
                    shop=shop_id, status="PAID"
                )
            elif order_type == "unpaid":
                orders = RestCheckout.objects.filter(
                    shop=shop_id, status="UNPAID"
                )

        args = {
            "orders": orders,
            "shop_id": shop_id,
            "order_type": order_type,
        }
        return render(request, "adminpanel/orders.html", args)
    else:
        return redirect("warning")

# Department


def departmentHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if shop_id.user == request.user:
        args = {
            "shop_id": shop_id
        }
        return render(request, "department/department.html", args)
    else:
        return redirect("warning")


def createDepartmentCategory(request):
    args = {

    }
    return render(request, "department/new-category.html", args)


def editDepartmentView(request):
    args = {

    }
    return render(request, "department/edit-department.html", args)


def createDepartmentView(request):
    args = {

    }
    return render(request, "department/new-department.html", args)


def createItemDepartmentView(request):
    args = {

    }
    return render(request, "department/new-item.html", args)

# Category


def categoryHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):
        category = Category.objects.filter(
            shop=shop_id,
        )
        args = {
            "shop_id": shop_id,
            "category": category,
        }
        return render(request, "category/category.html", args)
    else:
        return redirect("warning")


def editCategoryView(request, shop_id, cat_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):
        user_shops = Shop.objects.filter(user=shop_id.user, is_active=True)
        category_obj = get_object_or_404(Category, pk=cat_id)
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "user_shops": user_shops,
        "category_obj": category_obj
    }
    return render(request, "category/edit-category.html", args)


def adminEditCategoryView(request, shop_id, cat_id):
    cat_obj = get_object_or_404(Category, id=cat_id)
    trashCatObj = get_object_or_404(CategoryTrashModel, category=cat_obj)
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    # print("SHOP Name:", shop_obj.shop_name)

    if request.method == "POST":
        cat_name = request.POST.get("category_name")

        if cat_name:
            cat_obj.category_name = cat_name
            cat_obj.shop = shop_obj

            cat_obj.save()

            # Trash
            trashCatObj.category_name = cat_name
            trashCatObj.shop = shop_obj

            trashCatObj.save()

            return redirect(f"/adminpanel/category/{shop_id}/")
        else:
            return redirect(f"/adminpanel/edit-category/{shop_id}/{cat_id}/")


def createCategoryView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):

        shops = Shop.objects.filter(
            user=shop_id.user
        )

        if request.method == "POST":
            category_name = request.POST.get("category_name")
            shop = request.POST.get("shop")

            category = Category(
                category_name=category_name,
                shop=Shop.objects.get(id=shop_id.id)
            )

            category.save()

            # Trash
            t_category = CategoryTrashModel(
                category=category,
                category_name=category_name,
                shop=Shop.objects.get(id=shop_id.id)
            )

            t_category.save()

            return redirect(f"/adminpanel/category/{shop_id.id}/")

        args = {
            "shop_id": shop_id,
            "shops": shops
        }
        return render(request, "category/new-category.html", args)
    else:
        return redirect("warning")

# brand


def brandHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):
        brands = Brand.objects.filter(shop=shop_id)
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "brands": brands,
    }
    return render(request, "brand/brand.html", args)


def createBrand(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):
        args = {
            "shop_id": shop_id,
        }
        return render(request, "brand/new-brand.html", args)
    else:
        return redirect("warning")


def adminCreateBrand(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        brand_name = request.POST.get("brand_name")

        if brand_name:
            brand_obj = Brand(
                brand_name=brand_name,
                shop=shop_obj
            )
            brand_obj.save()

            # Trash
            t_brand = BrandTrashModel(
                brand=brand_obj,
                brand_name=brand_name,
                shop=shop_obj
            )
            t_brand.save()

            return redirect(f"/adminpanel/brand/{shop_obj.id}/")
        else:
            return redirect(f"/adminpanel/create-brand/{shop_obj.id}/")
    else:
        return redirect(f"/adminpanel/create-brand/{shop_obj.id}/")


def editBrandView(request, shop_id, brand_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory == True)):
        brand_obj = get_object_or_404(Brand, id=brand_id)
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "brand_obj": brand_obj,
    }
    return render(request, "brand/edit-brand.html", args)


def adminEditBrand(request, shop_id, brand_id):
    brand_obj = get_object_or_404(Brand, id=brand_id)
    shop = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop.is_active == False or expired_check == True:
        return redirect("warning")

    trashBrandObj = get_object_or_404(BrandTrashModel, brand=brand_obj)

    if request.method == "POST":
        brand_name = request.POST.get("brand_name")

        if brand_name:
            brand_obj.brand_name = brand_name
            brand_obj.shop = shop

            brand_obj.save()

            trashBrandObj.brand_name = brand_name
            trashBrandObj.shop = shop

            trashBrandObj.save()
        else:
            return redirect(f"/adminpanel/edit-brand/{shop_id}/{brand_id}/")

        return redirect(f"/adminpanel/brand/{shop_id}/")


def adminDeleteBrand(request, shop_id, brand_id):
    brand_obj = get_object_or_404(Brand, id=brand_id)
    brand_obj.delete()

    return redirect(f"/adminpanel/brand/{shop_id}/")


def newBrandItem(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
    }
    return render(request, "brand/new-brand-item.html", args)


def adminDeleteCategoryiew(request, shop_id, cat_id):
    category_obj = get_object_or_404(Category, id=cat_id)

    # print(category_obj)

    category_obj.delete()
    return redirect(f"/adminpanel/category/{shop_id}/")


def createCategoryItemView(request):
    args = {

    }
    return render(request, "category/new-category-item.html", args)

# Product


def productHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory)):
        products = Item.objects.filter(
            shop=shop_id
        )

        args = {
            "shop_id": shop_id,
            "products": products,
        }
        return render(request, "product/product.html", args)

    else:
        return redirect("warning")


def editProducteView(request, shop_id, prod_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")
    
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory)):
        prod_obj = get_object_or_404(Item, id=prod_id)
        categories = Category.objects.filter(shop=shop_id)
        vendors = Vendor.objects.filter(shop=shop_id)
        brands = Brand.objects.filter(shop=shop_id)
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "prod_obj": prod_obj,
        "categories": categories,
        "vendors": vendors,
        "brands": brands,
    }
    return render(request, "product/edit-product.html", args)


def adminEditProductView(request, shop_id, prod_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    prod_obj = get_object_or_404(Item, id=prod_id)
    trash_prod_obj = get_object_or_404(ItemTrashModel, item=prod_obj)
    vendor, selected_brand, upc, item_img, item_desc, item_b_price, item_sku, item_stock_q = None, None, None, None, None, 0.0, None, None
    out_of_stock = False

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_description = request.POST.get("product_description")
        get_category = request.POST.get("category")
        get_upc = request.POST.get("upc")
        sku = request.POST.get("sku")
        product_img = request.FILES.get("uploadImg")
        buying_price = request.POST.get("buying_price")
        selling_price = request.POST.get("selling_price")
        get_vendor = request.POST.get("get_vendor")
        get_brand = request.POST.get("brand")
        product_stock = request.POST.get("product_stock")
        get_out_of_stock = request.POST.get("out_of_stock")

        category = get_object_or_404(Category, id=get_category)
        
        if len(get_vendor) > 0:
            vendor = get_object_or_404(Vendor, id=get_vendor)

        if get_brand == "" or get_brand == "add-brand" or get_brand is None:
            selected_brand = None
        else:
            selected_brand = get_object_or_404(Brand, id=get_brand)

        if get_out_of_stock == "yes":
            out_of_stock = True

        if len(get_upc) > 0:
            upc = get_upc
        
        if product_img:
            item_img = product_img
            
        if len(product_description.strip()) > 0:
            item_desc = product_description
            
        if len(buying_price) > 0:
            item_b_price = buying_price
            
        if len(sku) > 0:
            item_sku = sku
            
        if len(product_stock) > 0:
            item_stock_q = product_stock

        if product_name and selling_price and category:
            if item_img is None:
                prod_obj.item_name = product_name
                prod_obj.item_price = selling_price
                prod_obj.buying_price = item_b_price
                prod_obj.brand = selected_brand
                prod_obj.category = category
                prod_obj.shop = shop_id
                prod_obj.stock_amount = item_stock_q
                prod_obj.out_of_stock = out_of_stock
                prod_obj.upc = upc
                prod_obj.sku = item_sku
                prod_obj.product_descriptions = item_desc

                trash_prod_obj.item_name = product_name
                trash_prod_obj.item_price = selling_price
                trash_prod_obj.buying_price = item_b_price
                trash_prod_obj.brand = selected_brand
                trash_prod_obj.category = category
                trash_prod_obj.shop = shop_id
                trash_prod_obj.stock_amount = item_stock_q
                trash_prod_obj.out_of_stock = out_of_stock
                trash_prod_obj.upc = upc
                trash_prod_obj.sku = item_sku
                trash_prod_obj.product_descriptions = item_desc
            else:
                prod_obj.item_name = product_name
                prod_obj.item_price = selling_price
                prod_obj.buying_price = item_b_price
                prod_obj.brand = selected_brand
                prod_obj.category = category
                prod_obj.shop = shop_id
                prod_obj.item_img = item_img
                prod_obj.stock_amount = item_stock_q
                prod_obj.out_of_stock = out_of_stock
                prod_obj.upc = upc
                prod_obj.sku = item_sku
                prod_obj.product_descriptions = item_desc

                trash_prod_obj.item_name = product_name
                trash_prod_obj.item_price = selling_price
                trash_prod_obj.buying_price = item_b_price
                trash_prod_obj.brand = selected_brand
                trash_prod_obj.category = category
                trash_prod_obj.shop = shop_id
                trash_prod_obj.item_img = item_img
                trash_prod_obj.stock_amount = item_stock_q
                trash_prod_obj.out_of_stock = out_of_stock
                trash_prod_obj.upc = upc
                trash_prod_obj.sku = item_sku
                trash_prod_obj.product_descriptions = item_desc
            
            if vendor:
                prod_obj.vendor = vendor
                trash_prod_obj.vendor = vendor
                
            prod_obj.save()
            trash_prod_obj.save()
        else:
            return redirect(f"/adminpanel/edit-product/{shop_id.id}/{prod_obj.id}/")
    return redirect(f"/adminpanel/product/{shop_id.id}/")


def createProducteView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_inventory)):      
        vendors = Vendor.objects.filter(shop=shop_id)

        get_upc, get_brand, vendor, item_img, item_desc, item_b_price, item_sku, item_stock_q = None, None, None, None, None, 0.0, None, None
        out_of_stock = False

        categories = Category.objects.filter(shop=shop_id)
        brands = Brand.objects.filter(shop=shop_id)

        if request.method == "POST":
            item_name = request.POST.get("item_name")
            product_description = request.POST.get("product_descriptions")
            brand = request.POST.get("brand")
            get_category = request.POST.get("category")
            upc = request.POST.get("upc")
            sku = request.POST.get("sku")
            product_stock = request.POST.get("product_stock")
            get_out_of_stock = request.POST.get("out_of_stock")
            uploadImg = request.FILES.get("uploadImg")
            buying_price = request.POST.get("buying_price")
            selling_price = request.POST.get("item_price")
            get_vendor = request.POST.get("vendor")

            if len(upc) > 0:
                get_upc = upc

            if get_out_of_stock == "yes":
                out_of_stock = True

            category = get_object_or_404(Category, id=get_category)

            if brand == "" or brand == "add-brand" or brand is None:
                get_brand = None
            else:
                get_brand = get_object_or_404(Brand, id=brand)

            if len(get_vendor) > 0:
                vendor = get_object_or_404(Vendor, id=get_vendor)
                
            if uploadImg:
                item_img = uploadImg
                
            if len(product_description.strip()) > 0:
                item_desc = product_description.strip()
                
            if len(buying_price) > 0:
                item_b_price = buying_price
            
            if len(sku) > 0:
                item_sku = sku
                
            if len(product_stock) > 0:
                item_stock_q = product_stock
                
            if item_name and category and selling_price:
                item_obj = Item(
                    item_name=item_name,
                    item_price=selling_price,
                    buying_price=item_b_price,
                    brand=get_brand,
                    category=category,
                    shop=shop_id,
                    stock_amount=item_stock_q,
                    out_of_stock=out_of_stock,
                    item_img=item_img,
                    upc=get_upc,
                    sku=item_sku,
                    product_descriptions=item_desc,
                )


                trashItemObj = ItemTrashModel(
                    item=item_obj,
                    item_name=item_name,
                    item_price=selling_price,
                    buying_price=item_b_price,
                    brand=get_brand,
                    category=category,
                    shop=shop_id,
                    stock_amount=item_stock_q,
                    out_of_stock=out_of_stock,
                    item_img=item_img,
                    upc=get_upc,
                    sku=item_sku,
                    product_descriptions=item_desc,
                )
                
                if vendor:
                    item_obj.vendor = vendor
                    trashItemObj.vendor = vendor

                item_obj.save()
                trashItemObj.save()

                return redirect(f"/adminpanel/product/{shop_id.id}/")
            else:
                return redirect(f"/adminpanel/create-product/{shop_id.id}/")
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "categories": categories,
        "brands": brands,
        "vendors": vendors,
    }
    return render(request, "product/new-product.html", args)


def deleteProductView(request, shop_id, prod_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        prod_obj = get_object_or_404(Item, id=prod_id, shop=shop_obj)
        prod_obj.delete()

        return redirect(f"/adminpanel/product/{shop_id}/")

# customer
def customerHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_customers)):
        customers = Customer.objects.filter(shop=shop_id)
        args = {
            "shop_id": shop_id,
            "customers": customers,
        }
        return render(request, "customers/customer.html", args)
    else:
        return redirect("warning")


def editCustomerView(request, shop_id, cust_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_customers == True)):
        customer_obj = get_object_or_404(Customer, id=cust_id)
        customer_obj = get_object_or_404(
            Customer, shop=shop_id, id=customer_obj.id)
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "customer_obj": customer_obj,
    }
    return render(request, "customers/edit-customer.html", args)


def adminEditCustomerView(request, shop_id, cust_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    customer_obj = get_object_or_404(Customer, id=cust_id)
    trashCustObj = get_object_or_404(CustomerTrashModel, customer=customer_obj)
    prev_email = customer_obj.customer_email

    if request.method == "POST":
        cust_name = request.POST.get("cust_name")
        cust_contact = request.POST.get("cust_contact")
        cust_email = request.POST.get("cust_email")
        cust_address = request.POST.get("cust_address")

        # Checking for email existence
        if prev_email != cust_email.strip():
            cust_obj_exists = Customer.objects.filter(customer_email=cust_email)
            if cust_obj_exists.exists():
                messages.error(request, "Customer email already exists!");
                return redirect(f"/adminpanel/edit-customer/{shop_id}/{cust_id}/")


        if cust_name and cust_contact and cust_email and cust_address:
            customer_obj.customer_name = cust_name
            customer_obj.customer_contact = cust_contact
            customer_obj.customer_email = cust_email
            customer_obj.customer_add = cust_address

            customer_obj.save()

            # Trash
            trashCustObj.customer_name = cust_name
            trashCustObj.customer_contact = cust_contact
            trashCustObj.customer_email = cust_email
            trashCustObj.customer_add = cust_address

            trashCustObj.save()

            return redirect(f"/adminpanel/customer/{shop_id}/")
        else:
            messages.error(request, "Some fields are not fulfilled properly!")
            return redirect(f"/adminpanel/edit-customer/{shop_id}/{cust_id}/")


def personalCustomerView(request):
    args = {

    }
    return render(request, "customers/personal-customer.html", args)


def businessCustomerView(request):
    args = {

    }
    return render(request, "customers/business-customer.html", args)


# vendor
def vendorView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_vendors == True)):
        vendors = Vendor.objects.filter(
            shop=shop_id
        )
        args = {
            "shop_id": shop_id,
            "vendors": vendors,
        }
        return render(request, "vendor/vendor.html", args)
    else:
        return redirect("warning")


def editVendorView(request, shop_id, vendor_id):
    vendorId = get_object_or_404(Vendor, id=vendor_id)
    trashVendorObj = get_object_or_404(VendorTrashModel, vendor=vendorId)
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    countrys = CountryModel.objects.all()
    citys = CityModel.objects.all()

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_vendors == True)):
        if request.method == "POST":
            vendor_name = request.POST.get("vendor_name")
            tax_id = request.POST.get("tax_id")
            shop = shop_id
            address = request.POST.get("address")
            country = request.POST.get("country")
            city = request.POST.get("city")
            zip_code = request.POST.get("zip_code")
            phone_number = request.POST.get("phone_number")
            contact_name = request.POST.get("contact_name")
            email = request.POST.get("email")
            website = request.POST.get("website")
            trade_license = request.POST.get("trade_license")

            if vendorId.vendor_name != vendor_name.strip():
                vendor_exist = Vendor.objects.filter(shop=shop_id, vendor_name=vendor_name.strip())
                
                if vendor_exist.exists():
                    messages.error(request, "Vendor name should be unique!")
                    return redirect(f"/adminpanel/edit-vendor/{shop_id.id}/{vendor_id}/")
                

            if vendor_name and address and country and city and phone_number and contact_name:
                vendorId.vendor_name = vendor_name
                vendorId.shop = shop
                vendorId.address = address
                vendorId.country = CountryModel.objects.get(country_name=country)
                vendorId.city = CityModel.objects.get(city_name=city)
                vendorId.zip_code = zip_code
                vendorId.phone_number = phone_number
                vendorId.contact_name = contact_name

                trashVendorObj.vendor_name = vendor_name
                trashVendorObj.shop = shop
                trashVendorObj.address = address
                trashVendorObj.country = CountryModel.objects.get(country_name=country)
                trashVendorObj.city = CityModel.objects.get(city_name=city)
                trashVendorObj.zip_code = zip_code
                trashVendorObj.phone_number = phone_number
                trashVendorObj.contact_name = contact_name

                if tax_id:
                    vendorId.tax_id = tax_id
                    trashVendorObj.tax_id = tax_id
                if email:
                    vendorId.email = email
                    trashVendorObj.email = email
                if website:
                    vendorId.website = website
                    trashVendorObj.website = website
                if trade_license:
                    vendorId.trade_license = trade_license
                    trashVendorObj.trade_license = trade_license

                vendorId.save()
                trashVendorObj.save()

                return redirect(f"/adminpanel/vendor/{shop_id.id}/")
    else:
        return redirect("warning")

    args = {
        "shop_id": shop_id,
        "vendorId": vendorId,
        "countrys": countrys,
        "citys": citys,
    }
    return render(request, "vendor/edit-vendor.html", args)


def createVendorView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    countrys = CountryModel.objects.all()
    citys = CityModel.objects.all()

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_vendors == True)):
        if request.method == "POST":
            vendor_name = request.POST.get("vendor_name")
            tax_id = request.POST.get("tax_id")
            shop = shop_id
            address = request.POST.get("address")
            country = request.POST.get("country")
            city = request.POST.get("city")
            zip_code = request.POST.get("zip_code")
            phone_number = request.POST.get("phone_number")
            contact_name = request.POST.get("contact_name")
            email = request.POST.get("email")
            website = request.POST.get("website")
            trade_license = request.POST.get("trade_license")

            vendor_exist = Vendor.objects.filter(shop=shop_id, vendor_name=vendor_name)

            if vendor_exist.exists():
                messages.error(request, "Vendor already exists!")
                return redirect(f"/adminpanel/create-vendor/{shop_id.id}")

            if vendor_name and address and country and city and phone_number and contact_name:
                vendor = Vendor(
                    vendor_name=vendor_name,
                    shop=shop,
                    address=address,
                    country=CountryModel.objects.get(country_name=country),
                    city=CityModel.objects.get(city_name=city),
                    phone_number=phone_number,
                    contact_name=contact_name,
                )

                if tax_id:
                    vendor.tax_id = tax_id
                if email:
                    vendor.email = email
                if website:
                    vendor.website = website
                if trade_license:
                    vendor.trade_license = trade_license
                if zip_code:
                    vendor.zip_code = zip_code

                tVendor = VendorTrashModel(
                    vendor=vendor,
                    vendor_name=vendor_name,
                    shop=shop,
                    address=address,
                    country=CountryModel.objects.get(country_name=country),
                    city=CityModel.objects.get(city_name=city),
                    phone_number=phone_number,
                    contact_name=contact_name,
                )

                if tax_id:
                    vendor.tax_id = tax_id
                    tVendor.tax_id = tax_id
                if email:
                    vendor.email = email
                    tVendor.email = email
                if website:
                    vendor.website = website
                    tVendor.website = website
                if trade_license:
                    vendor.trade_license = trade_license
                    tVendor.trade_license = trade_license
                if zip_code:
                    vendor.zip_code = zip_code
                    tVendor.zip_code = zip_code

                vendor.save()
                tVendor.save()
            else:
                vendor = Vendor(
                    vendor_name=vendor_name,
                    tax_id=tax_id,
                    shop=shop,
                    address=address,
                    country=country,
                    city=city,
                    zip_code=zip_code,
                    phone_number=phone_number,
                    contact_name=contact_name,
                    email=email,
                    trade_license=trade_license
                )
                vendor.save()

                tVendor = VendorTrashModel(
                    vendor_name=vendor_name,
                    tax_id=tax_id,
                    shop=shop,
                    address=address,
                    country=country,
                    city=city,
                    zip_code=zip_code,
                    phone_number=phone_number,
                    contact_name=contact_name,
                    email=email,
                    trade_license=trade_license
                )
                tVendor.save()

            return redirect(f"/adminpanel/vendor/{shop_id.id}/")
        args = {
            "shop_id": shop_id,
            "countrys": countrys,
            "citys": citys,
        }
        return render(request, "vendor/create-vendor.html", args)
    else:
        return redirect("warning")


def deleteVendorView(request, shop_id, vendor_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        vendor_obj = get_object_or_404(Vendor, id=vendor_id)
        vendor_obj.delete()

        return redirect(f"/adminpanel/vendor/{shop_obj.id}/")


# contact

def contactView(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    countries = CountryModel.objects.all()

    args = {
        "shop_id": shop_id,
        "countries": countries,
    }
    return render(request, "adminpanel/contact.html", args)


def submitContact(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    get_address2 = None

    if request.method == "POST":
        shop_name = request.POST.get("shop_name")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip = request.POST.get("zip")
        phone = request.POST.get("phone")
        country = request.POST.get("country")
        website = request.POST.get("website")
        email = request.POST.get("email")
        message = request.POST.get("message")

        shop = get_object_or_404(Shop, shop_name=shop_name)

        if len(address2) > 0:
            get_address2 = address2

        country = get_object_or_404(CountryModel, country_name=country)

        if shop_name and address1 and city and state and zip and country and website and email and message and phone:
            Contact.objects.create(
                shop=shop,
                address1=address1,
                address2=get_address2,
                city=city,
                state=state,
                zip=zip,
                country=country,
                website=website,
                email=email,
                message=message,
                phone=phone
            )
            messages.success(request, "Your message is sent successfully!")
            return redirect(f"/adminpanel/contact/{shop_id}/")
        else:
            return redirect(f"/adminpanel/home/{shop_id}/")


# exceptions
# success
def successView(request):
    args = {

    }
    return render(request, "exceptions/success.html", args)

# failed


def failedView(request):
    args = {

    }
    return render(request, "exceptions/failed.html", args)

# not found


def notFoundView(request):
    args = {

    }
    return render(request, "exceptions/notFound.html", args)

 # warning


def warningView(request):
    args = {

    }
    return render(request, "exceptions/warning.html", args)

# Export


def exportCustomerData(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["shop", "added_by", "customer_name", "customer_contact",
                    "customer_email", "customer_add", "created_at"])
    data = Customer.objects.filter(shop=shop_obj)
    for row in data:
        rowobj = [row.shop, row.added_by, row.customer_name, row.customer_contact,
                  row.customer_email, row.customer_add, row.created_at]
        writer.writerow(rowobj)
    return response


def exportProductData(request, shop_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["item_name", "item_price", "buying_price", "brand", "category", "vendor", "shop",
                    "stock_amount", "out_of_stock", "item_img", "product_descriptions", "upc", "sku", "created_at"])
    data = Item.objects.filter(shop=shop_id)
    for row in data:
        rowobj = [row.item_name, row.item_price, row.buying_price, row.brand, row.category, row.vendor, row.shop,
                  row.stock_amount, row.out_of_stock, row.item_img, row.product_descriptions, row.upc, row.sku, row.created_at]
        writer.writerow(rowobj)
    return response


def exportOrderData(request, shop_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["id", "created_at", "status",
                    "grand_total", "shop", "customer"])
    data = RestCheckout.objects.filter(shop=shop_id)
    for row in data:
        rowobj = [row.id, row.created_at, row.status,
                  row.grand_total, row.shop, row.customer]
        writer.writerow(rowobj)
    return response


def employeeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_emps == True)):
        emps = Employee.objects.filter(
            shop=shop_id.id
        )
        args = {
            "emps": emps,
            "shop_id": shop_id,
        }
        return render(request, "employee/employee.html", args)
    else:
        return redirect("warning")


def createEmployeeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    roles = Roles.objects.filter(shop=shop_id)
    message = None

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_emps == True)):
        if request.method == "POST":
            post_data = request.POST
            post_files = request.FILES
            full_name = post_data.get("full_name")
            emp_username = post_data.get("emp_username")
            emp_pin = post_data.get("emp_pin")
            confirm_pin = post_data.get("c_pin")
            emp_profile_pic = post_files.get("emp_profile_pic")
            is_active = request.POST.get("is_active")
            role = post_data.get("role")
            print(str(is_active))

            role = get_object_or_404(Roles, id=role)

            emp = Employee(
                shop=Shop.objects.get(id=shop_id.id),
                full_name=full_name,
                emp_username=emp_username,
                emp_pin=emp_pin,
                confirm_pin=confirm_pin,
                emp_profile_pic=emp_profile_pic,
                role=role,
                is_active=is_active
            )
            if emp_pin == confirm_pin:
                if len(emp_pin) >= 5:
                    emp.save()

                    # Trash
                    temp = EmployeeTrashModel(
                        shop=Shop.objects.get(id=shop_id.id),
                        employee=emp,
                        full_name=full_name,
                        emp_username=emp_username,
                        emp_pin=emp_pin,
                        confirm_pin=confirm_pin,
                        emp_profile_pic=emp_profile_pic,
                        role=role,
                        is_active=is_active
                    )
                    temp.save()

                    return redirect(f"/adminpanel/employee/{shop_id.id}/")
                else:
                    messages.error(request, "Pin is too short!")
                    return redirect(f"/adminpanel/create-employee/{shop_id.id}/")
            else:
                messages.error(request, "Password didn't matched!")
                return redirect(f"/adminpanel/create-employee/{shop_id.id}/")

        args = {
            "message": message,
            "shop_id": shop_id,
            "roles": roles,
        }
        return render(request, "employee/create-employee.html", args)
    else:
        return redirect("warning")


def editEmployeeView(request, emp_id, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    print(expired_check)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    empId = get_object_or_404(Employee, pk=emp_id)
    roles = Roles.objects.filter(shop=shop_id)
    trashEmpObj = get_object_or_404(EmployeeTrashModel, employee=empId)
    message = None

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_emps == True)):
        if request.method == "POST":
            emp_full_name = request.POST.get("full_name")
            emp_username = request.POST.get("emp_username")
            emp_pin = request.POST.get("emp_pin")
            confirm_pin = request.POST.get("c_pin")
            profile_pic = request.FILES.get("emp_profile_pic")
            role = request.POST.get("role")
            is_active = request.POST.get("is_active")

            if emp_pin != confirm_pin:
                messages.error(request, "Password didn't match!")
                return redirect(f"/adminpanel/edit-employee/{empId.id}/{shop_id.id}/")
            elif len(emp_pin) < 5:
                messages.error(request, "Pin is too short!")
                return redirect(f"/adminpanel/edit-employee/{empId.id}/{shop_id.id}/")

            role = get_object_or_404(Roles, id=role)

            if emp_full_name and emp_username and emp_pin and confirm_pin and role and is_active:
                empId.full_name = emp_full_name
                empId.emp_username = emp_username
                empId.emp_pin = emp_pin
                empId.confirm_pin = confirm_pin
                empId.role = role
                empId.is_active = is_active

                if profile_pic is not None:
                    empId.emp_profile_pic = profile_pic

                empId.save()

                # Trash
                trashEmpObj.full_name = emp_full_name
                trashEmpObj.emp_username = emp_username
                trashEmpObj.emp_pin = emp_pin
                trashEmpObj.confirm_pin = confirm_pin
                trashEmpObj.role = role
                trashEmpObj.is_active = is_active

                if profile_pic is not None:
                    trashEmpObj.emp_profile_pic = profile_pic

                trashEmpObj.save()
                return redirect(f"/adminpanel/employee/{shop_id.id}")

        args = {
            "shop_id": shop_id,
            "empId": empId,
            "roles": roles,
        }
        return render(request, "employee/edit-employee.html", args)
    else:
        return redirect("warning")


def deleteEmployeeView(request, emp_id, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    empId = get_object_or_404(Employee, pk=emp_id)

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_emps == True)):
        if request.method == "POST":
            empId.delete()
            return redirect(f"/adminpanel/employee/{shop_id}")
    else:
        return redirect("warning")


# Role Views
def roleViews(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")
        
    emp_session = request.session.get("employee_session", None)

    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_roles == True)):
        roles = Roles.objects.filter(
            shop=shop_id.id
        )
        args = {
            "roles": roles,
            "shop_id": shop_id,
        }
        return render(request, "roles/roles.html", args)
    else:
        return redirect("warning")


# Create role view
def createRolesView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_roles == True)):
        if request.method == "POST":
            role_title = request.POST.get("role_title")
            shop = Shop.objects.get(id=shop_id.id)
            is_admin = request.POST.get("is_admin")
            can_config_pos = request.POST.get("can_config_pos")
            can_config_roles = request.POST.get("can_config_roles")
            can_config_orders = request.POST.get("can_config_orders")
            can_config_inventory = request.POST.get("can_config_inventory")
            can_config_customers = request.POST.get("can_config_customers")
            can_config_vendors = request.POST.get("can_config_vendors")
            can_config_tables = request.POST.get("can_config_tables")
            can_config_emps = request.POST.get("can_config_emps")
            can_manage_settings = request.POST.get("can_manage_settings")

            if is_admin == "yes":
                is_admin = True
            else:
                is_admin = False
            if can_config_pos == "yes":
                can_config_pos = True
            else:
                can_config_pos = False
            if can_config_roles == "yes":
                can_config_roles = True
            else:
                can_config_roles = False
            if can_config_orders == "yes":
                can_config_orders = True
            else:
                can_config_orders = False
            if can_config_inventory == "yes":
                can_config_inventory = True
            else:
                can_config_inventory = False
            if can_config_customers == "yes":
                can_config_customers = True
            else:
                can_config_customers = False
            if can_config_vendors == "yes":
                can_config_vendors = True
            else:
                can_config_vendors = False
            if can_config_tables == "yes":
                can_config_tables = True
            else:
                can_config_tables = False
            if can_config_emps == "yes":
                can_config_emps = True
            else:
                can_config_emps = False
            if can_manage_settings == "yes":
                can_manage_settings = True
            else:
                can_manage_settings = False

            # Saving
            rl = Roles(
                role_title=role_title,
                shop=shop,
                is_admin=is_admin,
                can_config_pos=can_config_pos,
                can_config_roles=can_config_roles,
                can_config_orders=can_config_orders,
                can_config_inventory=can_config_inventory,
                can_config_customers=can_config_customers,
                can_config_vendors=can_config_vendors,
                can_config_tables=can_config_tables,
                can_config_emps=can_config_emps,
                can_manage_settings=can_manage_settings
            )
            rl.save()

            # Trash Role
            trl = RolesTrashModel(
                role=rl,
                role_title=role_title,
                shop=shop,
                is_admin=is_admin,
                can_config_pos=can_config_pos,
                can_config_roles=can_config_roles,
                can_config_orders=can_config_orders,
                can_config_inventory=can_config_inventory,
                can_config_customers=can_config_customers,
                can_config_vendors=can_config_vendors,
                can_config_tables=can_config_tables,
                can_config_emps=can_config_emps,
                can_manage_settings=can_manage_settings
            )
            trl.save()

            return redirect(f"/adminpanel/roles/{shop_id.id}/")

        args = {
            "shop_id": shop_id,
        }
        return render(request, "roles/create-role.html", args)
    else:
        return redirect("warning")


# Edit Roles View
def editRolesView(request, role_id, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    roleId = get_object_or_404(Roles, pk=role_id)
    trashRoleObj = get_object_or_404(RolesTrashModel, role=roleId)

    emp_obj = None

    emp_session = request.session.get("employee_session", None)

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_roles == True)):
        if request.method == "POST":
            roleId.shop = Shop.objects.get(id=shop_id.id)
            role_title = request.POST.get("role_title")
            is_admin = request.POST.get("is_admin")
            can_config_pos = request.POST.get("can_config_pos")
            can_config_roles = request.POST.get("can_config_roles")
            can_config_orders = request.POST.get("can_config_orders")
            can_config_inventory = request.POST.get("can_config_inventory")
            can_config_customers = request.POST.get("can_config_customers")
            can_config_vendors = request.POST.get("can_config_vendors")
            can_config_tables = request.POST.get("can_config_tables")
            can_config_emps = request.POST.get("can_config_emps")
            can_manage_settings = request.POST.get("can_manage_settings")

            if is_admin == "yes":
                is_admin = True
            else:
                is_admin = False
            if can_config_pos == "yes":
                can_config_pos = True
            else:
                can_config_pos = False
            if can_config_roles == "yes":
                can_config_roles = True
            else:
                can_config_roles = False
            if can_config_orders == "yes":
                can_config_orders = True
            else:
                can_config_orders = False
            if can_config_inventory == "yes":
                can_config_inventory = True
            else:
                can_config_inventory = False
            if can_config_customers == "yes":
                can_config_customers = True
            else:
                can_config_customers = False
            if can_config_vendors == "yes":
                can_config_vendors = True
            else:
                can_config_vendors = False
            if can_config_tables == "yes":
                can_config_tables = True
            else:
                can_config_tables = False
            if can_config_emps == "yes":
                can_config_emps = True
            else:
                can_config_emps = False
            if can_manage_settings == "yes":
                can_manage_settings = True
            else:
                can_manage_settings = False

            # Updating
            roleId.role_title = role_title
            roleId.is_admin = is_admin
            roleId.can_config_pos = can_config_pos
            roleId.can_config_roles = can_config_roles
            roleId.can_config_orders = can_config_orders
            roleId.can_config_inventory = can_config_inventory
            roleId.can_config_customers = can_config_customers
            roleId.can_config_vendors = can_config_vendors
            roleId.can_config_tables = can_config_tables
            roleId.can_config_emps = can_config_emps
            roleId.can_manage_settings = can_manage_settings

            roleId.save()
            # Updating Trash
            trashRoleObj.role_title = role_title
            trashRoleObj.is_admin = is_admin
            trashRoleObj.can_config_pos = can_config_pos
            trashRoleObj.can_config_roles = can_config_roles
            trashRoleObj.can_config_orders = can_config_orders
            trashRoleObj.can_config_inventory = can_config_inventory
            trashRoleObj.can_config_customers = can_config_customers
            trashRoleObj.can_config_vendors = can_config_vendors
            trashRoleObj.can_config_tables = can_config_tables
            trashRoleObj.can_config_emps = can_config_emps
            trashRoleObj.can_manage_settings = can_manage_settings

            trashRoleObj.save()

            return redirect(f"/adminpanel/roles/{shop_id.id}/")
        args = {
            "shop_id": shop_id,
            "roleId": roleId,

        }
        return render(request, "roles/edit-role.html", args)
    else:
        return redirect("warning")


# Delete Roles Views
def deleteRolesView(request, role_id, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    roleId = get_object_or_404(Roles, pk=role_id)

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_emps == True)):
        if request.method == "POST":
            roleId.delete()
            return redirect(f"/adminpanel/roles/{shop_id.id}/")
    else:
        return redirect("warning")
        
def viewShopSettings(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    package_obj = get_object_or_404(PackageCheckout, shop=shop_id)

    emp_session = request.session.get("employee_session", None)
    emp_obj = None
    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_manage_settings == True)):
        args = {
            "shop_id": shop_id,
            "package_obj": package_obj,
        }
        return render(request, "adminpanel/shop_settings.html", args)
    else:
        return redirect("warning")

# Update shop
def updateShopSettings(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    package_obj = get_object_or_404(PackageCheckout, shop=shop_id)

    prev_name = shop_obj.shop_name

    if request.method == "POST":
        cust_name = request.POST.get("cust_name")
        cust_phone = request.POST.get("cust_phone")
        shop_name = request.POST.get("shop_name")
        address1 = request.POST.get("add1")
        address2 = request.POST.get("add2")
        shop_phone = request.POST.get("shop_contact")
        shop_vat_id = request.POST.get("shop_vat_id")
        vat_amount = request.POST.get("vat_amount")
        mushak_check = request.POST.get("mushak_check")
        mushak_no = request.POST.get("mushak_no")
        shop_logo = request.FILES.get("shop_logo")
        shop_bin_no = request.POST.get("shop_bin_no")
        


        if prev_name != shop_name.strip():
            shop_exist = Shop.objects.filter(shop_name=shop_name)

            if shop_exist.exists():
                messages.error(request, "Shop name already exists! Please type another name")
                return redirect(f"/adminpanel/shop-settings/{shop_id}/")

        
        package_obj.customer_name = cust_name
        package_obj.customer_phone_number = cust_phone
        shop_obj.shop_name = shop_name
        shop_obj.shop_address1 = address1

        if len(address2.strip()):
            shop_obj.shop_address2 = address2
        
        shop_obj.shop_contact = shop_phone
        shop_obj.shop_vat = shop_vat_id
        shop_obj.vat_amount = vat_amount

        if mushak_check == "yes":
            shop_obj.show_mushak = True

            if len(mushak_no.strip()) <= 0:
                messages.error(request, "Mushak Number is required!")
                return redirect(f"/adminpanel/shop-settings/{shop_id}/")
            else:
                shop_obj.mushak_no = mushak_no
        else:
            shop_obj.show_mushak = False
            shop_obj.mushak_no = None

        shop_obj.shop_bin_no = shop_bin_no

        if shop_logo:
            shop_obj.shop_logo = shop_logo

        package_obj.save()
        shop_obj.save()

        return redirect(f"/adminpanel/home/{shop_id}/")


def adminDueOrdersView(request, shop_id):
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_orders == True)):
        orders = DueModel.objects.filter(
            shop=shop_id
        )

        args = {
            "orders": orders,
            "shop_id": shop_id,
        }
        return render(request, "adminpanel/due-checkout.html", args)
    else:
        return redirect("warning")

def adminTableOrdersView(request, shop_id):
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_orders == True)):
        orders = TableCheckout.objects.filter(
            shop=shop_id
        )

        args = {
            "orders": orders,
            "shop_id": shop_id,
        }
        return render(request, "adminpanel/table-checkout.html", args)
    else:
        return redirect("warning")

def adminAdvancedOrdersView(request, shop_id):
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_orders == True)):
        orders = AdvanceBookingModel.objects.filter(
            shop=shop_id
        )

        args = {
            "orders": orders,
            "shop_id": shop_id,
        }
        return render(request, "adminpanel/advance-order.html", args)
    else:
        return redirect("warning")

def exportDueData(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["sold_by", "created_at", "id", "shop", "customer",
                    "order_note", "submission_date", "due_total", "due_grand_total", "due_clear"])
    data = DueModel.objects.filter(shop=shop_obj)
    for row in data:
        rowobj = [row.sold_by, row.created_at, row.id, row.shop,
                  row.customer, row.order_note, row.submission_date, row.due_total, row.due_grand_total, row.due_clear]
        writer.writerow(rowobj)
    return response

def exportTableCheckoutData(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["sold_by", "created_at", "id", "customer_name", "customer_phone",
                    "table", "table_status", "discount", "amount_received", "change", "total", "grand_total", "shop"])
    data = TableCheckout.objects.filter(shop=shop_obj)
    for row in data:
        rowobj = [row.sold_by, row.created_at, row.id, row.customer_name, row.customer_phone,
                  row.table, row.table_status, row.discount, row.amount_received, row.change, row.total, row.grand_total, row.shop]
        writer.writerow(rowobj)
    return response

def exportAdvanceBookingData(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'
    writer = csv.writer(response)
    writer.writerow(["created_at", "id", "shop", "customer_name", "customer_phone", "customer_email", "notes", "number_of_people",
                    "advance_amount", "method", "account_number"])
    data = AdvanceBookingModel.objects.filter(shop=shop_obj)
    for row in data:
        rowobj = [row.created_at, row.id, row.shop, row.customer_name, row.customer_phone,
                  row.customer_email, row.notes, row.number_of_people, row.advance_amount, row.method, row.account_number]
        writer.writerow(rowobj)
    return response