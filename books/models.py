from django.db import models
from django.contrib.auth.models import User
from category.models import Category

# title, description,image, borrowing price, user reviews
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    details = models.TextField()
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books') 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    
    def __str__(self):
        return self.title
    
class Borrow_book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_boroow')
    buy_book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.buy_book.title
    

class Review(models.Model):
    STAR_RATINGS = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(default=0,choices=STAR_RATINGS)

    def __str__(self):
        return f"Reviews by : {self.name}"