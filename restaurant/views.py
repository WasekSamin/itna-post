from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import AdvanceBookingModel, CartItems, Category, Customer, Item, RestCheckout, DueModel, SellingSession, Table, TableCheckout, TableItems, RefundModel, Shop, Employee
from SAAS.models import *
from django.db.models import Q
import datetime
from datetime import date, datetime, timedelta
from django.contrib import messages
from TrashApp.models import *
from decimal import Decimal


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


def openRestaurantView(request, shop_id):
    # sessionId = get_object_or_404(SellingSession, pk=session_id)
    emp_obj = None
    
    emp_session = request.session.get("employee_session", None)
    print(emp_session)

    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")
   
    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        
        if emp_obj.shop != shopId:
            return redirect("warning")

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        if shopId.is_active == True:
            category = Category.objects.filter(
                shop=shop_id
            )
            items = Item.objects.filter(
                Q(out_of_stock=False) and Q(shop=shopId)
            )

            cart1 = request.session.get("cart1")
            remove = request.POST.get('remove')
            item_id = request.POST.get("item_id")

            ## Getting all customer

            customers = Customer.objects.filter(
                shop=shopId.id
            )

            if item_id is not None:
                if cart1:
                    quantity = cart1.get(item_id)
                    if quantity:
                        if remove:
                            cart1[item_id] = quantity - 1
                        else:
                            cart1[item_id] = quantity + 1
                    else:
                        cart1[item_id] = 1
                    if cart1[item_id] < 1:
                        cart1.pop(item_id)
                else:
                    cart1 = {}
                    cart1[item_id] = 1

                request.session['cart1'] = cart1

                return redirect(f"/restaurant/open-restaurant/{shop_id}/")
            
            # Getting All cart products

            if not cart1:
                request.session.cart1 = {}

            cart_products = None
            
            if cart1:
                ids = list(request.session.get('cart1').keys())
                
                cart_products = Item.get_items(ids)


            args = {
                "cart_products": cart_products,
                "items": items,
                "category": category,
                "customers": customers,
                "shopId": shopId,
                "emp_session": emp_session,
                "emp_obj": emp_obj,
                
                # "sessionId": sessionId,
            }
            return render(request, "restaurant/openRestaurant.html", args)
        else:
            return redirect("restaurant_failed")
    else:
        return redirect("warning")


def open_selling(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        if emp_obj.shop != shopId:
            return redirect("warning")

    if shopId.user == request.user or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        post_data = request.POST
        opening_text = post_data.get("opening_text")
        if request.method == "POST":
            ss = SellingSession(
                shop = Shop.objects.get(id=shopId.id),
                opening_text = opening_text,
            )
            ss.save()

            # Trash
            tss = SellingSessionTrashModel(
                shop = Shop.objects.get(id=shopId.id),
                selling_session=ss,
                opening_text = opening_text,
            )
            tss.save()
            return redirect(f"/restaurant/open-restaurant/{shopId.id}")
        args = {}
        return render(request, "restaurant/start_selling.html", args)
    else:
        return redirect("warning")


def close_selling(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        total_sold = request.POST.get("total_sold")
        total_sold = float(total_sold)
        print(total_sold, type(total_sold))
        session_id = SellingSession.objects.filter(shop=shopId, closing_date=None)

        print("ALL SESSION IDs:", session_id)

        for item in session_id:
            print(item.id)

        if session_id.exists():
            session_id = session_id.first()
            print("GET SESSION ID:", session_id.id)
            print("HEllo session" + str(session_id))
            session_id.closing_text = "Closed Successfully!"
            session_id.closing_date = date.today()
            # session_id.closing_date = date.today
            session_id.total_sold = total_sold
            session_id.save()

            # Trash
            sstm = SellingSessionTrashModel.objects.filter(selling_session=session_id, shop=shopId, closing_date=None)

            if sstm.exists():
                sstm = sstm.last()
                print("GET SESSION ID:", sstm)
                print("HEllo session" + str(sstm))
                sstm.closing_text = "Closed Successfully!"
                sstm.closing_date = date.today()
                # session_id.closing_date = date.today
                sstm.total_sold = total_sold
                sstm.save()


            emp_session = request.session.get("employee_session", None)

            if emp_session is not None:
                del request.session["employee_session"]

            return redirect(f"/adminpanel/logout/")
        else:
            return redirect(f"/restaurant/start-selling-session/{shopId.id}/")

            

def restaurantDueView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_obj = None
    emp_session = request.session.get("employee_session", None)

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        # if request.user == "AnonymousUser":
        #     customers = Customer.objects.filter(shop=shopId, added_by=emp_obj)
        # else:
        customers = Customer.objects.filter(shop=shopId)

        cart1 = request.session.get("cart1", None)
        cart_products = None
        
        if cart1 is not None:
            ids = list(request.session.get('cart1').keys())
            cart_products = Item.get_items(ids)

        if request.method == "POST":
            customer = request.POST.get("selected_due_user")
            order_note = request.POST.get("order_note")
            submission_date = request.POST.get("order_submission_due_date")
            due_total = request.POST.get("due_total")
            items = cart_products
            print(due_total)

            year = submission_date.split("/")[2]
            month = submission_date.split("/")[0]
            day = submission_date.split("/")[1]

            submission_date = f"{year}-{month}-{day}"

            # print(submission_date)
            
            if cart_products is None or len(items) <= 0:
                return redirect(f"/restaurant/due-restaurant/{shop_id}/")

            due = DueModel(
                sold_by=emp_obj,
                customer=Customer.objects.get(id=customer),
                order_note=order_note,
                submission_date=submission_date,
                shop=shopId,
            )

            due.save()

            # Trash
            td = DueTrashModel(
                dueObj=due,
                sold_by=emp_obj,
                customer=Customer.objects.get(id=customer),
                order_note=order_note,
                submission_date=submission_date,
                shop=shopId,
            )

            td.save()

            total_price = 0

            for item in items:
                quantity = cart1.get(str(item.id))
                total_price += item.item_price * quantity
                cartItems = CartItems(
                    item=item,
                    quantity=quantity
                )
                cartItems.save()
                due.items.add(cartItems)
            
            due.due_total = total_price
            td.due_total = total_price

            if shopId.vat_amount > 0:
                due.due_grand_total = total_price + total_price * Decimal(shopId.vat_amount / 100)
                td.due_grand_total = total_price + total_price * Decimal(shopId.vat_amount / 100)
            else:
                due.due_grand_total = total_price
                td.due_grand_total = total_price

            due.save()
            td.save()

            # Clearing cookie
            cart1 = {}
            request.session["cart1"] = cart1

            return redirect(f"/restaurant/open-restaurant/{shop_id}/")

        args = {
            "cart_products": cart_products,
            "customers": customers,
            "shopId": shopId,
        }
        return render(request, "restaurant/openRestaurantDue.html", args)
    else:
        return redirect("warning")



def restaurantAvailableTableView(request, shop_id):
    pass
    # shopId = get_object_or_404(Shop, id=shop_id)
    # args = {
    #     "shopId": shopId,
    # }
    # return render(request, "restaurant/availableTable.html", args)

# Add ing new Customer Function
def addingNewCustomer(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        if request.method == "POST":
            data = request.POST
            shop = shop_id
            try:
                added_by = emp_obj
            except:
                added_by = None

            customer_name = data.get('customer_name')
            customer_contact = data.get('customer_contact')
            customer_email = data.get('customer_email')
            customer_add = data.get('customer_add')
            email_exits = Customer.objects.filter(customer_email=customer_email)
            if not email_exits.exists():
                c_obj = Customer(
                    shop=shop,
                    added_by = added_by,
                    customer_name = customer_name,
                    customer_contact = customer_contact,
                    customer_email = customer_email,
                    customer_add = customer_add
                )
                c_obj.save()

                # Trash
                cst = CustomerTrashModel(
                    customer=c_obj,
                    shop=shop,
                    added_by = added_by,
                    customer_name = customer_name,
                    customer_contact = customer_contact,
                    customer_email = customer_email,
                    customer_add = customer_add
                )
                cst.save()

                return redirect(f"/restaurant/open-restaurant/{shop_id.id}/")
            else:
                messages.error(request, "Customer email already exists!");
                return redirect(f"/restaurant/open-restaurant/{shop_id.id}/")
                
        args = {
            "shop_id": shop_id,
        }
        return render(request, "restaurant/openRestaurant.html", args)
    else:
        return redirect("warning")

# Checkout Function

def get_checkout(request, shop_id):
    cart1 = request.session.get("cart1")
    shopId = Shop.objects.get(pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        if emp_obj.shop != shopId:
            return redirect("warning")

    if request.method == "POST":
        if cart1:
            ids = list(request.session.get('cart1').keys())

            if len(ids) <= 0:
                return redirect(f"/restaurant/open-restaurant/{shop_id}/")

            cart_products = Item.get_items(ids)
            items = cart_products
            # customer = request.POST.get("customer")
            amount_received = request.POST.get("amount_received")
            customerId = request.POST.get("customer_id")
            discount = request.POST.get("discount")
            credit_card_number = request.POST.get("credit_card_number")
            bkash_number = request.POST.get("bkash_number")
            nagad_number = request.POST.get("nagad_number")

            payment_method, payment_number = None, None

            
            if len(credit_card_number) > 0 or len(bkash_number) or len(nagad_number):
                if len(credit_card_number) > 0:
                    payment_method = "Credit Card"
                    payment_number = credit_card_number
                elif len(bkash_number) > 0:
                    payment_method = "bKash"
                    payment_number = bkash_number
                elif len(nagad_number) > 0:
                    payment_method = "Nagad"
                    payment_number = nagad_number
            else:
                payment_method="CASH"

            if customerId or customerId != "":
                checkout = RestCheckout(
                    sold_by=emp_obj,
                    customer=Customer.objects.get(id=customerId),
                    amount_received=amount_received,
                    discount=discount,
                    shop=shopId,
                    status="PAID",
                    payment_method=payment_method,
                    payment_number=payment_number
                )
                checkout.save()

                trash_checkout = RestCheckoutTrashModel(
                    rest_checkout=checkout,
                    sold_by=emp_obj,
                    customer=Customer.objects.get(id=customerId),
                    amount_received=amount_received,
                    discount=discount,
                    shop=shopId,
                    status="PAID",
                    payment_method=payment_method,
                    payment_number=payment_number
                )
                trash_checkout.save()
            else:
                checkout = RestCheckout(
                    sold_by=emp_obj,
                    customer=None,
                    amount_received=amount_received,
                    discount=discount,
                    shop=shopId,
                    status="PAID",
                    payment_method=payment_method,
                    payment_number=payment_number
                )
                checkout.save()

                trash_checkout = RestCheckoutTrashModel(
                    rest_checkout=checkout,
                    sold_by=emp_obj,
                    customer=None,
                    amount_received=amount_received,
                    discount=discount,
                    shop=shopId,
                    status="PAID",
                    payment_method=payment_method,
                    payment_number=payment_number
                )
                trash_checkout.save()

            grand_total = 0
            for item in items:
                quantity = cart1.get(str(item.id))
                grand_total += item.item_price * quantity
                cartItems = CartItems(
                    item=item,
                    quantity=quantity
                )
                cartItems.save()
                checkout.items.add(cartItems)
            
            if float(discount) > 0:
                grand_total = grand_total - (grand_total * Decimal(float(discount) / 100.0))

            checkout.total = grand_total
            trash_checkout.total = grand_total

            if shopId.vat_amount > 0:
                checkout.grand_total = grand_total + (grand_total * Decimal(shopId.vat_amount / 100.0))
                trash_checkout.grand_total = grand_total + (grand_total * Decimal(shopId.vat_amount / 100.0))
            else:
                checkout.grand_total = grand_total
                trash_checkout.grand_total = grand_total

            checkout.change = checkout.grand_total - Decimal(checkout.amount_received)
            trash_checkout.change = checkout.grand_total - Decimal(checkout.amount_received)

            checkout.save()
            trash_checkout.save()
            # Clearing cookie
            cart1 = {}
            request.session["cart1"] = cart1
            return redirect(f"/restaurant/restaurant-receipt/{shop_id}/{checkout.id}/")
        
    args = {
        "shopId": shopId
    }
    return render(request, "restaurant/openRestaurant.html", args)

# Delete product
def deleteRestaurantProductView(request, shop_id, id):
    cart1 = request.session.get("cart1", None)
    shopId = Shop.objects.get(pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    product_id = str(id)

    if request.method == "POST":
        if cart1:
            cart1.pop(product_id)

            request.session["cart1"] = cart1
            # print(cart1)
        return redirect(f"/restaurant/open-restaurant/{shop_id}/")


def restaurantAllPaymentsView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        if emp_obj.shop != shopId:
            return redirect("warning")


    if shopId.user == request.user or emp_obj is not None:      
        orders = RestCheckout.objects.filter(shop=shopId)
        
        args = {
            "orders": orders,
            "shopId": shopId,
        }
        return render(request, "restaurant/restaurantAllPayments.html", args)

    else:
        return redirect("warning")

def restaurantAllDuesView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")
    
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        if emp_obj.shop != shopId:
            return redirect("warning")

    
    if shopId.user == request.user or emp_obj is not None:
        dues = DueModel.objects.filter(shop=shopId)
        
        args = {
            "dues": dues,
            "shopId": shopId,
        }
        return render(request, "restaurant/restaurantAllDues.html", args)

    else:
        return redirect("warning")


def restaurantOrderDetailsView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    order_details = get_object_or_404(RestCheckout, shop=shopId, id=id)

    args = {
        "order_details": order_details,
        "shopId": shopId,
    }
    return render(request, "restaurant/orderDetails.html", args)

def restaurantDueOrderDetailsView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    order_details = get_object_or_404(DueModel, shop=shopId, id=id)

    args = {
        "order_details": order_details,
        "shopId": shopId,
    }
    return render(request, "restaurant/restaurantDueOrderDetails.html", args)

def restaurantDueUpdateStatus(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    order_details = get_object_or_404(DueModel, shop=shopId, id=id)

    if request.method == "POST":
        payment_status = request.POST.get("payment_status")

        if payment_status == "clear":
            order_details.due_clear = True
        elif payment_status == "not_clear":
            order_details.due_clear = False
        order_details.save()
        
        return redirect(f"/restaurant/due-details/{shop_id}/{id}/")



# restaurant receipt
def restaurantReceiptView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    order_details = RestCheckout.objects.get(id=id)

    total_item = 0
    
    for item in order_details.items.all():
        total_item += item.quantity

    args = {
        "order_details": order_details,
        "total_item": total_item,
        "shopId": shopId,
    }
    return render(request, "restaurant/restaurantReceipt.html", args)

# restaurant receipt
def restaurantDueReceiptView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    order_details = get_object_or_404(DueModel, id=id, shop=shopId)
    print(order_details)

    total_item = 0
    
    for item in order_details.items.all():
        total_item += item.quantity

    args = {
        "order_details": order_details,
        "total_item": total_item,
        "shopId": shopId,
    }
    return render(request, "restaurant/restaurantDueReceipt.html", args)


# selecting the customer or walkin

def select_customer_or_walkin(request, id):
    get_customerId = Customer.objects.get(pk=id)
    
    args = {
        "get_customerId": get_customerId
    }
    return render(request, "restaurant/openRestaurant.html", args)


def get_table_page(request, shop_id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
    

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        tables = Table.objects.filter(
            is_active = True,
            shop=shopId
        )
        args = {
            "shopId": shopId,
            "tables": tables,
        }
        return render(request, "restaurant/availableTable.html", args)
    else:
        return redirect("warning")

def get_table_details(request, shop_id, id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        table_id = Table.objects.get(pk=id)
        category = Category.objects.filter(
                shop=shopId
            )
        items = Item.objects.filter(
                Q(out_of_stock=False) and Q(shop=shopId)
            )
        cart2 = request.session.get("cart2")
        remove = request.POST.get('remove')
        item_id = request.POST.get("item_id")

        ## Getting all customer

        customers = Customer.objects.filter(
            shop=shopId.id
        )

        if item_id is not None:
            if cart2:
                quantity = cart2.get(item_id)
                if quantity:
                    if remove:
                        cart2[item_id] = quantity - 1
                    else:
                        cart2[item_id] = quantity + 1
                else:
                    cart2[item_id] = 1
                if cart2[item_id] < 1:
                    cart2.pop(item_id)
            else:
                cart2 = {}
                cart2[item_id] = 1

            request.session['cart2'] = cart2

            return redirect(f"/restaurant/table-details/{shop_id}/{table_id.id}/")
        
        # Getting All cart products

        if not cart2:
            request.session.cart2 = {}

        cart_products2 = None
        
        if cart2:
            ids = list(request.session.get('cart2').keys())
           
            cart_products2 = Item.get_items(ids)

        args = {
            "tableId": table_id,
            "category": category,
            "items": items,
            "cart_products2": cart_products2,
            "shopId": shopId,
        }
        return render(request, "table/table_cart.html", args)
    else:
        return redirect("warning")


def table_checkout_validation(request, id, shop_id, *args, **kwargs):
    cart2 = request.session.get("cart2", None)
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    tableId = get_object_or_404(Table, pk=id)
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
        if emp_obj.shop != shopId:
            return redirect("warning")


    if request.method == "POST":
        ids = list(request.session.get('cart2').keys())

        if len(ids) <= 0:
            return redirect("open-restaurant")

        if cart2 is not None:
            cart_products2 = Item.get_items(ids)
            items = cart_products2
            customer_name = request.POST.get("customer_name")
            customer_phone = request.POST.get("customer_phone")
            table = tableId
            amount_received = request.POST.get("amount_received")
            customerId = request.POST.get("customer_id")
            discount = request.POST.get("discount")
        
            table_checkout = TableCheckout(
                sold_by=emp_obj,
                customer_name=customer_name,
                customer_phone=customer_phone,
                table=table,
                table_status="PAID",
                discount=discount,
                amount_received=amount_received,
                shop=shopId,
            )
            table_checkout.save()

            total = 0
            for item in items:
                quantity = cart2.get(str(item.id))
                total += item.item_price * quantity
                tableItems = TableItems(
                    items=item,
                    quantity=quantity
                )
                tableItems.save()
                table_checkout.item_item.add(tableItems)
            
            if float(discount) > 0:
                total = total - (total * Decimal(float(discount) / 100.0))

            table_checkout.total = total

            if shopId.vat_amount > 0:
                table_checkout.grand_total = total + total * Decimal(shopId.vat_amount / 100)
            else:
               table_checkout.grand_total = total

            table_checkout.change = table_checkout.grand_total - Decimal(table_checkout.amount_received)

            table_checkout.save()
            # Clearing cookie
            cart2 = {}
            request.session["cart2"] = cart2
            return redirect(f"/restaurant/table-details/{shop_id}/{tableId.id}/")
    
def tableOrderDetailsView(request, shop_id, table_id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    tableObj = get_object_or_404(TableCheckout, id=table_id)

    args={
        "shopId": shopId,
        "tableObj": tableObj,
    }
    return render(request, "table/table_order_details.html", args) 

def get_table_orders(request, shop_id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        get_table_orders = TableCheckout.objects.filter(
            shop=shopId
        )
        args = {
            "shopId": shopId,
            "get_table_orders": get_table_orders,
        }
        return render(request, "table/all_table_order.html", args)
    else:
        return redirect("warning")



def get_table_receipt(request, shop_id, id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        get_receipt = TableCheckout.objects.get(pk=id)
        get_table_orders = TableCheckout.objects.filter(
            shop=shopId
        )
        
        args = {
            "shopId": shopId,
            "get_receipt": get_receipt,
            "get_table_orders": get_table_orders,
        }
        return render(request, "table/table_order_details.html", args)
    else:
        return redirect("warning")

def get_table_order_print(request, shop_id, id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        order_details = get_object_or_404(TableCheckout, pk=id, shop=shopId)
        total_item = 0
    
        for item in order_details.item_item.all():
            total_item += item.quantity
        args = {
            "order_details": order_details,
            "shopId": shopId,
            "total_item": total_item,
        }
        return render(request, "table/table_order_print.html", args)
    else:
        return redirect("warning")


def closeRegisterView(request, shop_id):
    shopId = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    args = {
        "shopId": shopId,
    }
    return render(request, "restaurant/closeRegister.html", args)


def get_refund_or_post_refund(request, order_id, shop_id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        orderId = RestCheckout.objects.get(pk=order_id)
        if orderId is not None:
            if request.method == "POST":
                order = orderId
                refund_total = request.POST.get("refund_total")
                shop = shopId

                refund_obj = RefundModel(
                    order=order,
                    refund_total=refund_total,
                    shop=shop,
                    refund_by=emp_obj
                )
                refund_obj.save()

                # Trash
                tr = RefundTrashModel(
                    refundObj=refund_obj,
                    order=order,
                    refund_total=refund_total,
                    shop=shop,
                    refund_by=emp_obj
                )
                tr.save()

                return redirect("success")

        else:
            return redirect("warning")        
        args = {}
        return render(request, "restaurant/refund.html", args)
    else:
        return redirect("warning")


def advance_booking(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shopId)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shopId.is_active == False or expired_check == True:
        return redirect("warning")

    advances = AdvanceBookingModel.objects.filter(
        shop=shopId
    )
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shopId.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_pos == True)):
        if request.method == "POST":
            post_data = request.POST
            customer_name = post_data.get("customer_name")
            customer_phone = post_data.get("customer_phone")
            customer_email = post_data.get("customer_email")
            notes = post_data.get("notes")
            advance_amount = post_data.get("advance_amount")
            account_number = post_data.get("acount_number")
            num_of_people = request.POST.get("number_of_people")
            payment_method = None

            credit_card_number = request.POST.get("credit_card_number")
            bkash_number = request.POST.get("bkash_number")
            nagad_number = request.POST.get("nagad_number")

            if len(credit_card_number) > 0 or len(bkash_number) or len(nagad_number) > 0:
                if len(credit_card_number) > 0:
                    payment_method = "CREDIT CARD"
                    account_number = credit_card_number
                elif len(bkash_number) > 0:
                    payment_method = "BKASH"
                    account_number = bkash_number
                elif len(nagad_number) > 0:
                    payment_method = "NAGAD"
                    account_number = nagad_number
            else:
                payment_method = "CASH"
                
            if customer_name and customer_phone and customer_email and num_of_people and advance_amount:
                advance_model = AdvanceBookingModel(
                    shop=Shop.objects.get(id=shopId.id),
                    customer_name = customer_name,
                    customer_phone = customer_phone,
                    customer_email = customer_email,
                    advance_amount = advance_amount,
                    method = payment_method,
                    account_number = account_number,
                    number_of_people=num_of_people
                )

                # Trash
                tadv = AdvanceBookingTrashModel(
                    advanceBooking=advance_model,
                    shop=Shop.objects.get(id=shopId.id),
                    customer_name = customer_name,
                    customer_phone = customer_phone,
                    customer_email = customer_email,
                    advance_amount = advance_amount,
                    method = payment_method,
                    account_number = account_number,
                    number_of_people=num_of_people
                )

                if notes:
                    advance_model.notes = notes
                    tadv.notes = notes

                advance_model.save()
                tadv.save()
                return redirect(f"/restaurant/tables/{shopId.id}/")

        args = {
            "shopId": shopId,
            "advances": advances,
        }
        return render(request, "restaurant/advance_booking.html", args)
    else:
        return redirect("warning")


# Admin table
def allTablesView(request, shop_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    all_tables = None

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        all_tables = Table.objects.filter(shop=shop_id)
    else:
        return redirect("warning")


    args = {
        "shop_id": shop_id,
        "all_tables": all_tables,
    }
    return render(request, "table/adminAllTables.html", args)

def deleteTableView(request, shop_id, table_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    if request.method == "POST":
        table_obj = get_object_or_404(Table, id=table_id)
        table_obj.delete()
        return redirect(f"/adminpanel/all-tables/{shop_id}/")

# Edit table
def editTableView(request, shop_id, table_id):
    shop_id = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_id)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_id.is_active == False or expired_check == True:
        return redirect("warning")

    table_obj, waiters = None, None
    
    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)            

    if (shop_id.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        table_obj = get_object_or_404(Table, id=table_id)
        waiters = Employee.objects.filter(shop=shop_id, is_active="ACTIVE")
    else:
        return redirect("warning")


    args = {
        "shop_id": shop_id,
        "table_obj": table_obj,
        "waiters": waiters,
    }
    return render(request, "table/adminEditTable.html", args)

def adminEditTableView(request, shop_id, table_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    make_active_table = False
    get_table_obj = get_object_or_404(Table, id=table_id)
    trashTableObj = get_object_or_404(TableTrashModel, table=get_table_obj)

    if request.method == "POST":
        table_name = request.POST.get("table_name")
        is_active = request.POST.get("is_active")
        waiter_id = request.POST.get("waiter")
        num_of_chairs = request.POST.get("chair_number")

        if is_active == "yes":
            make_active_table = True
        else:
            make_active_table = False

        table_obj = Table.objects.filter(table_name=table_name, shop=shop_obj)

        if table_obj.exists():
            table_obj = table_obj.last()

            if table_obj.table_name != get_table_obj.table_name.strip():
                messages.error(request, "Table name should be unique!")
                return redirect(f"/adminpanel/edit-table/{shop_id}/{table_id}/")

        if table_name and waiter_id:
            waiter_obj = get_object_or_404(Employee, id=waiter_id)

            get_table_obj.table_name = table_name.strip()
            get_table_obj.is_active = make_active_table
            get_table_obj.waiter = waiter_obj
            get_table_obj.shop = shop_obj
            get_table_obj.number_of_chairs = num_of_chairs

            get_table_obj.save()

            # Trash
            trashTableObj.table_name = table_name.strip()
            trashTableObj.is_active = make_active_table
            trashTableObj.waiter = waiter_obj
            trashTableObj.shop = shop_obj

            trashTableObj.save()

            return redirect(f"/adminpanel/all-tables/{shop_id}/")
        else:
            messages.error(request, f"Error in editing table {get_table_obj}!")
            return redirect(f"/adminpanel/edit-table/{shop_id}/{table_id}/")

# Create table
def createTable(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    emp_session = request.session.get("employee_session", None)
    emp_obj = None

    if emp_session is not None:
        emp_obj = get_object_or_404(Employee, emp_username=emp_session)
            
    
    if (shop_obj.user == request.user) or (emp_obj is not None and (emp_obj.role.is_admin == True or emp_obj.role.can_config_tables == True)):
        waiters = Employee.objects.filter(shop=shop_obj, is_active="ACTIVE")
    else:
        return redirect("warning")


    args = {
        "shop_obj": shop_obj,
        "waiters": waiters,
    }
    return render(request, "table/create_table.html", args)

# Admin create table
def adminCreateTableView(request, shop_id):
    shop_obj = get_object_or_404(Shop, id=shop_id)

    package_checkout_obj = get_object_or_404(PackageCheckout, shop=shop_obj)
    expired_check = packageExpiredCheck(package_checkout_obj)

    if shop_obj.is_active == False or expired_check == True:
        return redirect("warning")

    make_active_table = False

    if request.method == "POST":
        table_name = request.POST.get("table_name")
        is_active = request.POST.get("is_active")
        waiter_id = request.POST.get("waiter")
        num_of_chairs = request.POST.get("chair_number")

        table_obj = Table.objects.filter(table_name=table_name, shop=shop_obj)

        # Should get a unique table name
        if table_obj.exists():
            messages.error(request, "Table name should be unique!")
            return redirect(f"/adminpanel/create-table/{shop_id}/")

        if is_active == "yes":
            make_active_table = True
        else:
            make_active_table = False

        if table_name and waiter_id:
            table_name = table_name.strip()
            waiter_obj = get_object_or_404(Employee, id=waiter_id)

            table_obj = Table(table_name=table_name, is_active=make_active_table, shop=shop_obj, number_of_chairs=num_of_chairs, waiter=waiter_obj)
            table_obj.save()

            # Trash
            tt = TableTrashModel(
                table=table_obj,
                table_name=table_name,
                is_active=make_active_table, 
                shop=shop_obj, 
                waiter=waiter_obj)
            tt.save()

            return redirect(f"/adminpanel/all-tables/{shop_id}/")
        else:
            messages.error(request, "Error in creating table!")
            return redirect(f"/adminpanel/create-table/{shop_id}/")

def failedView(request):
    return render(request, "restaurant_exceptions/failed.html")

def successView(request):
    return render(request, "restaurant_exceptions/success.html")