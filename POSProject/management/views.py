from fnmatch import filter

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.utils.datetime_safe import datetime

from sale.models import Order, Order_Products, Product, Type

from . import models

# Create your views here.

def my_login(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('login')
        else:
            context['username'] = username
            context['password'] = password
    return render(request, template_name='management/login.html', context=context)

def my_signup(request):
    return render(request, template_name='management/signup.html')

# ดูว่าที่ add เพิ่มเคยมีแล้วหรือยัง


def index(request):
    editT = False
    editP = False
    typeEdit = Type.objects.all()
    typelist = Type.objects.all().order_by('name')
    editProduct = Product.objects.all()

    searchN = request.GET.get('searchN', '') #name
    searchT = request.GET.get('searchT', '') #type
    submit_btn = request.GET.get('submit_btn', '')

    productNE = request.GET.get('productNE', '') #name
    productDE = request.GET.get('productDE', '') #name
    productTE = request.GET.get('productTE', '') #type
    productPE = request.GET.get('productPE', '') #name
    productAE = request.GET.get('productAE', '') #name
    productIE = request.GET.get('productIE', '') #name

    productN = request.GET.get('productN', '') #name
    productD = request.GET.get('productD', '') #name
    productT = request.GET.get('productT', '') #type
    productP = request.GET.get('productP', '') #name
    productA = request.GET.get('productA', '') #name
    
    typeN = request.GET.get('typeN', '') #name
    typeD = request.GET.get('typeD', '') #type

    typeND = request.GET.get('typeND', '') #name

    typeNE = request.GET.get('typeNE', '') #name
    typeDE = request.GET.get('typeDE', '') #name

    if submit_btn == 'search':
        products = Product.objects.filter(
            Q(name__icontains=searchN) &
            Q(type__name__icontains=searchT)
            ).order_by('name')
        

    elif submit_btn == 'all': 
        products = Product.objects.all().order_by('name')
        searchN = ''
        searchT = ''

    elif submit_btn == 'edit_product':
        productE = Product(id=productIE)
        productE.name = productNE
        productE.description = productDE
        productE.type_id = Type.objects.get(name=productTE)
        productE.price = productPE
        productE.amount = productAE
        productE.save()

    elif submit_btn.startswith('E'):
        editP = True
        editProduct = Product.objects.get(id=int(submit_btn.strip('E')))

    elif submit_btn.startswith('R'):
        submit_btns = submit_btn.strip('R')
        pro = Product.objects.get(id=int(submit_btns))
        
        pro.delete()
    
    elif submit_btn == 'add_product':
        if Product.objects.filter(name=productN):
            pass
        else:
            newProduct = Product(name=productN, description=productD, price=productP, amount=productA, type_id=Type.objects.get(name=productT).id)
            newProduct.save()

    elif submit_btn == 'add_type':
        if Type.objects.filter(name=typeN):
            pass
        else:
            newType = Type(name=typeN, description=typeD)
            newType.save()

    elif submit_btn == 'delete_type':
        if typeNE  and typeDE:
            editT = False
        else:
            deleteType = Type.objects.filter(name=typeND)
            deleteType.delete()
        

    elif submit_btn == 'edit_type':
        if (typeNE  or typeDE) and Type.objects.filter(name=typeND):
            typeEdit = Type.objects.get(name=typeND)
            if typeNE and typeDE:
                typeEdit.name = typeNE
                typeEdit.description = typeDE
                typeEdit.save()
            elif typeNE:
                typeEdit.name = typeNE
                typeEdit.save()
            else:
                typeEdit.description = typeDE
                typeEdit.save()
         
        else:
            try:
                typeEdit = Type.objects.get(name=typeND)
                editT = True
            except Exception:
                editT = True

    if submit_btn != 'all':
        products = Product.objects.filter(
                Q(name__icontains=searchN) &
                Q(type__name__icontains=searchT)
                ).order_by('name')
        typelist = Type.objects.all().order_by('name')

    else:
        products = Product.objects.all().order_by('name')
        typelist = Type.objects.all().order_by('name')
    
    
    
    return render(request, template_name='management/manage-page.html', context={
        'product': products,
        'searchN': searchN,
        'searchT': searchT,
        'typelist': typelist,
        'editT': editT,
        'editP': editP,
        'typeEdit': typeEdit,
        'editProduct': editProduct
        })





def product_list(request):
    """
        แสดงข้อมูล student ทั้งหมดในระบบ
    """
    search = request.GET.get('search', '')
