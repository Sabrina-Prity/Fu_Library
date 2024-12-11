from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('details/<int:id>', views.DetailsBookView.as_view(), name = 'details_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
]
