from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from urllib.parse import quote
from .models import Category, Product, CartItem, Order, OrderItem, SpecialOrder, Review
from .forms import SignupForm, SpecialOrderForm, CheckoutForm, ReviewForm

def home(request):
    categories = Category.objects.all()
    featured = Product.objects.filter(is_available=True, is_featured=True)[:8]
    latest = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:6]
    return render(request, 'core/home.html', {
        'categories': categories, 'featured': featured, 'latest': latest, 'reviews': reviews
    })

def shop(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_available=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    categories = Category.objects.all()
    return render(request, 'core/shop.html', {'products': products, 'categories': categories, 'query': query})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_available=True)
    return render(request, 'core/category_detail.html', {'category': category, 'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to leave a review.')
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.product = product
            r.user = request.user
            r.save()
            messages.success(request, 'Thank you! Your review was added.')
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()
    related = Product.objects.filter(category=product.category, is_available=True).exclude(pk=pk)[:4]
    return render(request, 'core/product_detail.html', {'product': product, 'reviews': reviews, 'form': form, 'related': related})

def about(request):
    return render(request, 'core/about.html')

# --- AUTH ---
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to House of Nissi!')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Wrong username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- CART ---
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(i.total() for i in items)
    return render(request, 'core/cart.html', {'items': items, 'total': total})

@login_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    action = request.GET.get('action')
    if action == 'plus':
        item.quantity += 1
        item.save()
    elif action == 'minus':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    return redirect('cart')

# --- CHECKOUT - LOGIN REQUIRED ---
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('shop')
    total = sum(i.total() for i in items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()
            for i in items:
                OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity, price=i.product.price)
            items.delete()
            messages.success(request, f'Order #{order.id} placed! Pay with {order.payment_method} and send reference.')
            return redirect('my_orders')
    else:
        form = CheckoutForm(initial={'full_name': request.user.username})
    return render(request, 'core/checkout.html', {'form': form, 'items': items, 'total': total})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    specials = SpecialOrder.objects.all().order_by('-created_at')
    return render(request, 'core/my_orders.html', {'orders': orders, 'specials': specials})

def track_order(request):
    order = None
    if request.GET.get('order_id'):
        try:
            order = Order.objects.get(id=request.GET.get('order_id'))
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Check ID.')
    return render(request, 'core/track_order.html', {'order': order})

# --- SPECIAL ORDER -> WHATSAPP + ADMIN ---
def special_order(request):
    if request.method == 'POST':
        form = SpecialOrderForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            # Build WhatsApp message
            text = f"Hello House of Nissi! NEW SPECIAL ORDER\n\nName: {obj.name}\nPhone: {obj.phone}\nFabric: {obj.fabric}\nSize: {obj.size}\nBudget: {obj.budget}\nDesign: {obj.design_details}"
            wa = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(text)}"
            messages.success(request, 'Special Order saved! You will now be taken to WhatsApp.')
            return render(request, 'core/special_order_success.html', {'wa_link': wa, 'order': obj})
    else:
        form = SpecialOrderForm()
    return render(request, 'core/special_order.html', {'form': form})