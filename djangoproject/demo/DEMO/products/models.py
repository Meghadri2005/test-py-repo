from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def average_rating(self):
        """Calculate average rating from all reviews"""
        reviews = self.reviews.all()
        if reviews.count() == 0:
            return 0
        return sum(review.rating for review in reviews) / reviews.count()

    def review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    helpful_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']
