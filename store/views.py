from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

def home(request):
    trending_products=Product.objects.filter(trending=1)
    context={"trending_products":trending_products}
    return render(request, 'store/home.html',context)

def collection(request):
    category =Category.objects.filter(status=0)
    context={'category':category}
    return render(request,"store/collection.html",context)

def collectionview(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products = Product.objects.filter(category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
        context={'products':products,'category_name':category_name}
        return render(request,'store/products/home.html',context)
    else:
        messages.warning(request,"No such Category Found!")
        return redirect("collection")

def productview(request,cate_slug,prod_slug):
    if Category.objects.filter(slug=cate_slug,status=0).exists():
        if Product.objects.filter(category__slug=cate_slug,slug=prod_slug,status=0).exists():
            products = Product.objects.filter(category__slug=cate_slug,slug=prod_slug,status=0).first()
            context={'products':products}
        else:
            messages.error(request,"No such product found!")
            return redirect('collection')
    else:
        messages.error(request,"No such Category found!")
        return redirect('collection')
    return render(request,"store/products/view.html",context)
