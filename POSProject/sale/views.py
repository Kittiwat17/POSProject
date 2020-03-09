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
    return render(request, template_name='sale/login.html', context=context)

def my_signup(request):
    return render(request, template_name='sale/signup.html')




def index(request):
    typelist = Type.objects.all().order_by('name')
    prices = 0
    datetimes = datetime.now()
    try:
        order_product = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0)).order_by('id')
    except Exception:
        Order(total_price=0,date_time=datetimes).save()
        
        order_product = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0)).order_by('id')


    searchN = request.GET.get('searchN', '') #name
    searchT = request.GET.get('searchT', '') #type
    submit_btn = request.GET.get('submit_btn', '')
#    add_remove = request.GET.get('add_remove', '')
    

    if submit_btn == 'search':
        products = Product.objects.filter(
            Q(name__icontains=searchN) &
            Q(type__name__icontains=searchT)
            ).order_by('name')
        

    elif submit_btn == 'all': 
        products = Product.objects.all().order_by('name')
        searchN = ''
        searchT = ''

    elif submit_btn.startswith('R') & submit_btn.endswith('A'):
        submit_btns = submit_btn.lstrip('R')
        submit_btns = submit_btns.rstrip('A')
        pro = Product.objects.get(id=int(submit_btns))
        order_pro = Order_Products.objects.get(order_id=Order.objects.get(total_price=0),product_id=Product.objects.get(id=int(submit_btns)))
                
        
        pro.amount = pro.amount + order_pro.amount
        pro.save()
        order_pro.delete()
        order_product = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0)).order_by('id')
        

    elif submit_btn.startswith('A'):
        submit_btns = submit_btn.strip('A')
        pro = Product.objects.get(id=int(submit_btns))
            
        try:
            order = Order.objects.get(total_price=0)
        except Exception:
            order = Order(total_price=0,date_time=datetimes)
            order.save()
        if pro.amount - 1 >= 0:
            if Order_Products.objects.filter(order_id=Order.objects.get(total_price=0),product_id=Product.objects.get(id=int(submit_btns))):
                order_in = Order_Products.objects.get(order_id=Order.objects.get(total_price=0),product_id=Product.objects.get(id=int(submit_btns)))
                order_in.amount = order_in.amount + 1
                order_in.save()
            
 
            else:   
                order_in = Order_Products(order_id=order,product_id=Product.objects.get(id=int(submit_btns)),amount=1)
                order_in.save()
            
            pro.amount = pro.amount - 1
            pro.save()
            order_product = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0)).order_by('id')
        
        
    
    elif submit_btn.startswith('R'):
        submit_btns = submit_btn.strip('R')
        pro = Product.objects.get(id=int(submit_btns))
        order_pro = Order_Products.objects.get(order_id=Order.objects.get(total_price=0),product_id=Product.objects.get(id=int(submit_btns)))
                
        if order_pro.amount <= 1:
            order_pro.delete()
        else:
            order_pro.amount = order_pro.amount - 1
            order_pro.save()
        pro.amount = pro.amount + 1
        pro.save()

    elif submit_btn == 'clear_cart':
        order_in = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0))
        for ord in order_in:
            pro = Product.objects.get(id=int(ord.product_id.id))
            pro.amount = pro.amount + ord.amount
            pro.save()
        order_in.delete()

    

    elif submit_btn == 'sale':
        try:
            order = Order.objects.get(total_price=0)
        except Exception:
            order = Order(total_price=0,date_time=datetimes)
            order.save()
        for price in order_product:
            prices = prices + (price.product_id.price  *  price.amount)  
        
        if order_product:
            order = Order.objects.get(total_price=0)
            # for p in order_product:
            #     p.in_cart = False
            #     p.save()
                #orderP = Order_Products(order_id=order,product_id=Product.objects.get(id=int(p.product_id.id)),amount=p.amount)
                #orderP.save()
                #p.delete()
            order.total_price = prices
            order.date_time = datetimes
            order.save()

            Order(total_price=0,date_time=datetimes).save()
            order_product = Order_Products.objects.filter(order_id=Order.objects.get(total_price=0)).order_by('id')

    prices = 0  
    for price in order_product:
        prices = prices + (price.product_id.price  *  price.amount)    
    

    if submit_btn != 'all':
        products = Product.objects.filter(
                Q(name__icontains=searchN) &
                Q(type__name__icontains=searchT)
                ).order_by('name')

    else:
        products = Product.objects.all().order_by('name')

    
    
    
    return render(request, template_name='sale/index.html', context={
        'product': products,
        'searchN': searchN,
        'searchT': searchT,
        'order_product': order_product,
        'prices': prices,
        'typelist': typelist
        })





def product_list(request):
    """
        แสดงข้อมูล student ทั้งหมดในระบบ
    """
    search = request.GET.get('search', '')
