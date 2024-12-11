from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import BuyingHistory


def registration(request):
    if request.method == 'POST':
       register_form = forms.RegistrationForm(request.POST)
       if register_form.is_valid():
           register_form.save()
           messages.success(request, 'Account Created SuccessFully')
           return redirect('deposit')
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'user/registration.html', {'form': register_form, 'type': 'Registration'})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=name, password=password)  # Checking user in the database
                if user is not None:
                    messages.success(request, 'Logged In Successfully')
                    login(request, user)
                    return redirect('deposit')
            else:
                messages.warning(request, 'Login information incorrect, Please try again.')  # For form validation failure
        else:
            form = AuthenticationForm()
        return render(request, 'user/registration.html', {'form': form, 'type': 'Login'})




def user_logout(request):
    logout(request)
    return redirect('user_login')



@login_required
def user_profile(request):
    data = Book.objects.filter(user = request.user)
    return render(request, 'user/profile.html', {'data':data})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile')
    
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
    return render(request, 'user/edit_profile.html', {'form' : profile_form})



@login_required
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password Change Successfully')
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user = request.user)
        return render(request, 'user/change_pass.html', {'form':form})
    else:
        return redirect('user_login')
    
# @login_required
# def buy_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     if book.quantity > 0:
#         book.quantity -= 1
#         book.save()
        
#         # Record purchase
#         BuyingHistory.objects.create(user=request.user, book=book)
#         messages.success(request, f"You successfully bought the {book.title}!")
#     else:
#         messages.error(request, f"Sorry, the {book.title} is out of stock.")

#     return redirect('buying_history') 

# @login_required
# def buying_history(request):
#     buying_history = BuyingHistory.objects.filter(user=request.user).select_related('book')

#     return render(request, 'user/buying_history.html', {'buying_history': buying_history})



