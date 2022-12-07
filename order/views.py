# Create your views here.
from cart.cart import Cart
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

# for HTML Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Order, OrderItem, OrderUpdate

# checkout view
def checkout(
    request,
    first_name,
    last_name,
    email,
    address,
    zipcode,
    place,
    phone,
    payment,
    amount,
):
    order = Order.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        zipcode=zipcode,
        place=place,
        phone=phone,
        payment=payment,
        amount=amount,
        customers=request.user,
    )
    update = OrderUpdate(id=order.id, update_desc="The order has been placed")
    update.save()
    for item in Cart(request):
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            vendor=item["product"].vendor,
            customer=request.user,
            price=item["product"].price,
            quantity=item["quantity"],
        )
        order.vendors.add(item["product"].vendor)
    return order


# email notification to vendor about order
def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM
    for vendor in order.vendors.all():
        to_email = vendor.email
        subject = "Customer Has placed an Order"
        text_content = "You have a new order!"
        html_content = render_to_string(
            "order/email_notifyorder_vendor.html", {"order": order, "vendor": vendor}
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# email notification to customer about order
def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM
    to_email = order.email
    subject = "Order confirmation"
    text_content = "Thank you for the order!"
    html_content = render_to_string(
        "order/email_notifyorder_customer.html", {"order": order}
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# order tracker for customer
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get("orderId", "")
        email = request.POST.get("email", "")
        try:
            order = Order.objects.filter(id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(id=orderId)
                updates = []
                for item in update:
                    updates.append({"Status": item.update_desc, "time": item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse(
                    "Please Enter the same OrderID and Email to track your order."
                )
        except Exception as e:
            return HttpResponse("Enter your correct Order ID and Email")
    return render(request, "order/trackorder.html")
