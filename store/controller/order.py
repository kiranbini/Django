from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Product, Cart, Wishlist
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, Wishlist,Profile,Order,OrderItem


def order_view(request):
    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request,"store/order.html",context)

def view_order(request,t_no):
    order=Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems=OrderItem.objects.filter(order=order)
    context={'orderitems':orderitems,'order':order}
    return render(request,"store/orderitems.html",context)
