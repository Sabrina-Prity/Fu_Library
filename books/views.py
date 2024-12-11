from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from . import forms
from . import models
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import Book, Borrow_book, Review
from account.models import Deposit
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

@method_decorator(login_required, name='dispatch')
class AddBookView(CreateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('add_book')
    def form_valid(self, form):
        messages.success(self.request, 'Book Added Successfully')
        form.instance.user = self.request.user
        return super().form_valid(form)
        


@method_decorator(login_required, name='dispatch')
class DetailsBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'books/book_details.html'

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        review_form = forms.ReviewForm(data=request.POST)
        
        # Check if the user has borrowed the book
        if not Borrow_book.objects.filter(user=request.user, buy_book=book).exists():
            return redirect('details_book', id=book.id)  # Redirect to prevent reviewing if not borrowed

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.post = book  # Link review to the book
            new_review.user = request.user  # Associate review with the current user
            new_review.save()

            # Optionally, add a success message
            messages.success(request, "Your review has been successfully submitted.")
        
        return self.get(request, *args, **kwargs)  # Re-render the page with the review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object  # The Book object from the detail view
        reviews = book.reviews.all()
        review_form = forms.ReviewForm()

        # Check if the user has borrowed this book
        has_borrowed = Borrow_book.objects.filter(user=self.request.user, buy_book=book).exists()

        context["reviews"] = reviews
        context["review_form"] = review_form
        context["has_borrowed"] = has_borrowed  # Add this to check in the template
        return context

    


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_deposit = Deposit.objects.get(user=request.user)

    if user_deposit.balance >= book.price and book.quantity > 0:
        # Deduct balance and decrease quantity
        user_deposit.balance -= book.price
        user_deposit.save()

        book.quantity -= 1
        book.save()

        # Create borrow record
        Borrow_book.objects.create(user=request.user, buy_book=book)

        messages.success(request, f"You have successfully borrowed '{book.title}'.")
        return redirect('borrowed_books')
    else:
        messages.info(request, "You do not have enough balance. Please deposit first")
        return redirect('details_book', id = book_id)
    
     
@login_required
def borrowed_books(request):
    borrowed_books = Borrow_book.objects.filter(user=request.user)
    user_deposit = Deposit.objects.get(user=request.user)
    total_amount = sum(b.buy_book.price for b in borrowed_books)

    return render(request, 'books/borrowed_books.html', {
        'borrowed_books': borrowed_books,
        'balance': user_deposit.balance,
        'total_amount': total_amount,
    })
    
        

@login_required
def return_book(request, borrow_id):
    borrow_record = get_object_or_404(Borrow_book, id=borrow_id)
    user_deposit = Deposit.objects.get(user=request.user)

    # Refund balance and increase quantity
    user_deposit.balance += borrow_record.buy_book.price
    user_deposit.save()

    borrow_record.buy_book.quantity += 1
    borrow_record.buy_book.save()

    borrow_record.delete()

    messages.success(request, f"You have successfully returned '{borrow_record.buy_book.title}'.")
    return redirect('borrowed_books')
    
    
    