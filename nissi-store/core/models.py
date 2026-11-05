from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('dresses', 'Dresses'),
        ('bags', 'Bags'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
    ]
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage?")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, default="Pay on Delivery")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('signup', 'Signed Up'),
        ('login', 'Logged In'),
        ('view_product', 'Viewed Product'),
        ('add_cart', 'Added to Cart'),
        ('place_order', 'Placed Order'),
        ('report_issue', 'Reported Issue'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    details = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - {self.action}"

class SupportTicket(models.Model):
    STATUS_CHOICES = [('open','Open'),('in_progress','In Progress'),('resolved','Resolved')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    admin_reply = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.subject} - {self.user.username}"

class SiteSetting(models.Model):
    announcement = models.CharField(max_length=200, default="FREE DELIVERY IN ACCRA ON ORDERS OVER GH₵ 500")
    whatsapp_number = models.CharField(max_length=20, default="233550100199")
    def __str__(self):
        return "Site Settings"