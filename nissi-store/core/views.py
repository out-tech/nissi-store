from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order, OrderItem, Customer, ActivityLog, SupportTicket, SiteSetting

def get_setting():
    s, _ = SiteSetting.objects.get_or_create(id=1)
    return s

def home(request):
    products = Product.objects.filter(is_featured=True)[:8]
    if not products:
        products = Product.objects.all()[:8]
    return render(request, 'home.html', {'products': products, 'setting': get_setting()})

def shop(request):
    category = request.GET.get('category', '')
    q = request.GET.get('q', '')
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if q:
        products = products.filter(name__icontains=q)
    return render(request, 'shop.html', {'products': products, 'setting': get_setting(), 'category': category})

def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        ActivityLog.objects.create(user=request.user, action='view_product', details=f"Viewed {p.name}")
    related = Product.objects.filter(category=p.category).exclude(pk=pk)[:4]
    return render(request, 'product_detail.html', {'p': p, 'related': related, 'setting': get_setting()})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        else:
            user = User.objects.create_user(username=username, password=password)
            Customer.objects.create(user=user, phone=phone)
            ActivityLog.objects.create(user=user, action='signup', details=f"{username} signed up")
            login(request, user)
            return redirect('/')
    return render(request, 'signup.html', {'setting': get_setting()})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            ActivityLog.objects.create(user=user, action='login', details="Logged in")
            return redirect('/')
        else:
            messages.error(request, 'Wrong username or password')
    return render(request, 'login.html', {'setting': get_setting()})

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=pid)
            sub = p.price * qty
            total += sub
            items.append({'product': p, 'qty': qty, 'sub': sub})
        except: pass
    return render(request, 'cart.html', {'items': items, 'total': total, 'setting': get_setting()})

@login_required
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    p = get_object_or_404(Product, pk=pk)
    ActivityLog.objects.create(user=request.user, action='add_cart', details=f"Added {p.name} to cart")
    return redirect('/cart/')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/shop/')
    total = 0
    for pid, qty in cart.items():
        p = Product.objects.get(pk=pid)
        total += p.price * qty
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total, phone=request.POST.get('phone'), address=request.POST.get('address'), payment_method=request.POST.get('payment', 'Pay on Delivery'))
        for pid, qty in cart.items():
            p = Product.objects.get(pk=pid)
            OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
            p.stock -= qty
            p.save()
        cust, _ = Customer.objects.get_or_create(user=request.user)
        cust.total_orders += 1
        cust.total_spent += total
        cust.save()
        ActivityLog.objects.create(user=request.user, action='place_order', details=f"Placed Order #{order.id} - GH₵{total}")
        request.session['cart'] = {}
        return redirect('/my-orders/')
    return render(request, 'checkout.html', {'total': total, 'setting': get_setting()})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my-orders.html', {'orders': orders, 'setting': get_setting()})

@login_required
def support_view(request):
    if request.method == 'POST':
        SupportTicket.objects.create(user=request.user, subject=request.POST.get('subject'), message=request.POST.get('message'))
        ActivityLog.objects.create(user=request.user, action='report_issue', details=request.POST.get('subject'))
        messages.success(request, 'Your issue has been sent. Madam Nissi will reply soon.')
        return redirect('/support/')
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support.html', {'tickets': tickets, 'setting': get_setting()})