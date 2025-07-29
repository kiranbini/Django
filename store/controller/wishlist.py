from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from store.models import Product, Cart, Wishlist
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='loginpage')
def index(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    context={'wishlist':wishlist}
    return render(request,"store/wishlist.html",context)

def addtoWishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product added to wishlist"})
            else:
                return JsonResponse({'status': 'No such product found'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('/')

def deletewishlistitem(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            try:
                wishlist_item = Wishlist.objects.filter(user=request.user, product_id=prod_id)
                wishlist_item.delete()
                return JsonResponse({'status': 'Product removed from wishlist'})
            except Wishlist.DoesNotExist:
                return JsonResponse({'status': 'Product not found in wishlist'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    return redirect('/')



