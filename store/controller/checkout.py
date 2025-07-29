from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Product, Cart, Wishlist,Profile,Order,OrderItem
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random


@login_required(login_url='loginpage')
def index(request):
    rawcart=Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty>item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitem=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cartitem:
        total_price=total_price+item.product.selling_price+item.product_qty
    context={'cartitem':cartitem,'total_price':total_price }
    return render(request,"store/checkout.html",context)



@login_required(login_url="loginpage")
def placeorder(request):
    if request.method == "POST":
        currentuser = User.objects.filter(id=request.user.id).first()


        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user).exists():
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('Phone')
            userprofile.address = request.POST.get('Address')
            userprofile.city = request.POST.get('City')
            userprofile.state = request.POST.get('State')
            userprofile.country = request.POST.get('Country')
            userprofile.pincode = request.POST.get('PinCode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('firstname')
        neworder.lname = request.POST.get('lastname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('Phone')
        neworder.address = request.POST.get('Address')
        neworder.city = request.POST.get('City')
        neworder.state = request.POST.get('State')
        neworder.country = request.POST.get('Country')
        neworder.pincode = request.POST.get('PinCode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(item.product.selling_price * item.product_qty for item in cart)

        neworder.total_price = cart_total_price
        trackno = "Varsha" + str(random.randint(111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = "Varsha" + str(random.randint(111111, 9999999))

        neworder.tracking_no = trackno
        neworder.save()

        for item in cart:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully!")

        payMode = request.POST.get('payment_mode')
        if payMode == "Paid by Razorpay":
            return JsonResponse({'status': "Your order has been placed successfully!"})
        return redirect('order')

        return redirect('/')

@login_required(login_url="loginpage")
def razorpaycheck(request):
    cart=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price=item.product.selling_price + item.product_qty
    return JsonResponse({'total_price':total_price})
