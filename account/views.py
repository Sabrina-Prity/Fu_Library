from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import CreateView, ListView,FormView
from .forms import DepositForm, UserRegistrationForm
from django.contrib.auth.models import User
from .models import Deposit


# Utility function to send email notifications
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
        'current_balance': user.user_account.balance + amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()



class UserRegistrationView(CreateView):
    model = User
    template_name = 'account/registration_form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self,form):
        # form.save()
        messages.success(self.request,f"Account Created Successfully!.")
        return super().form_valid(form)
       
    
    
    
class UserLoginView(LoginView):
    template_name = 'account/registration_form.html'
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
    def form_valid(self,form):
        messages.success(self.request,'loged in successfull!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request,f'Your loged in information incorrect')
        return super().form_invalid(form)
    
    
   
def UserLogoutview(request):
    logout(request)
    return redirect('login')

class DepositMoneyView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        try:
            # Check if the user has a Deposit account
            account = self.request.user.user_account
        except Deposit.DoesNotExist:
            # If the user doesn't have a Deposit, create one
            account = Deposit.objects.create(user=self.request.user, account_no=11000 + self.request.user.id)
            messages.success(self.request, "A deposit account has been created for you!")

        form = DepositForm()
        return render(request, 'account/deposit_form.html', {
            "form": form,
            'title': 'Deposit Form',
            'account': account
        })

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST":
            form = DepositForm(self.request.POST)
            if form.is_valid():
                amount = form.cleaned_data.get('balance')
                try:
                    account = Deposit.objects.get(user=self.request.user)
                    account.balance += amount
                    account.balance_after_tranjections = account.balance
                    account.save()

                    # Send email notification
                    mail_subject = "Deposit Messages"
                    message = render_to_string('account/deposite_email.html', {
                        'user': self.request.user,
                        'amount': amount,
                        'nowbalance': account.balance
                    })
                    send_email = EmailMultiAlternatives(mail_subject, "", to=[self.request.user.email])
                    send_email.attach_alternative(message, 'text/html')
                    send_email.send()

                    messages.success(self.request, f"Successfully deposited {amount}tk.")
                    return redirect('deposit')
                except Deposit.DoesNotExist:
                    # If for some reason the deposit is missing, create a new one
                    Deposit.objects.create(user=self.request.user, account_no=11000 + self.request.user.id)
                    messages.error(self.request, "Deposit account was missing, but it has been created. Please try again.")
                    return redirect('deposit')
            
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["title"] = 'Deposit Form' 
    #     return context