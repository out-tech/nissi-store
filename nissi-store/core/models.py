from django.db import models
from django.contrib.auth.models import User

# Admin adds this herself. NO preset categories.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Admin types emoji or icon name: e.g. 👗 👜 👠 👔 🧥 💍
    icon = models.CharField(max_length=10, default="👗", help_text="Put emoji e.g 👗 👜 👠")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.product.price * self.quantity

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('MTN MoMo', 'MTN MoMo'),
        ('Telecel Cash', 'Telecel Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Paystack', 'Paystack - Card / Bank'),
        ('Pay on Delivery', 'Pay on Delivery'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='MTN MoMo')
    payment_reference = models.CharField(max_length=100, blank=True, help_text="MoMo Transaction ID / Paystack Ref")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_feedback = models.TextField(blank=True, help_text="Admin reply to customer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class SpecialOrder(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Replied', 'Replied'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    design_details = models.TextField(help_text="How they want their cloth designed")
    fabric = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=50, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='special_orders/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    admin_feedback = models.TextField(blank=True, help_text="Admin feedback to customer")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Special Order - {self.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(5,'⭐⭐⭐⭐⭐'),(4,'⭐⭐⭐⭐'),(3,'⭐⭐⭐'),(2,'⭐⭐'),(1,'⭐')], default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"