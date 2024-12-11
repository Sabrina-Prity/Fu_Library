from django.shortcuts import render, get_object_or_404
from books.models import Book
from category.models import Category

def home(request, category_slug=None):
    # Get all books
    data = Book.objects.all()

    # Initialize category_list regardless of the condition
    category_list = Category.objects.all()

    # If a category_slug is provided, filter books by that category
    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        data = Book.objects.filter(category=category)

    return render(request, 'core/home.html', {'data': data, 'category_list': category_list})
