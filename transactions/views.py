# Create your views here.
from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Transaction
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# ======================TRANSACTIONS SECTION=============================#







class TransactionHomeView(ListView):
    model = Transaction
    template_name = 'transactions/transactionshome.html'
    context_object_name = 'transactions'





class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'transactions/transactions_form.html'
    fields = [
    'clients_name',
    'loan_given',
    'loan_balance',
    'repayment',
    'fines',
    'agreed_shedule',
    'weekly_shedule',
    'defaulted_days',
    'residence',
    'loan_collateral',
    'id_number',
    'phone',
    ]

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin,  UpdateView):
    model = Transaction
    template_name = 'transactions/transactions_form.html'
    fields = [
    'clients_name',
    'loan_given',
    'loan_balance',
    'repayment',
    'fines',
    'agreed_shedule',
    'weekly_shedule',
    'defaulted_days',
    'residence',
    'loan_collateral',
    'id_number',
    'phone',
    ]
    # form verification

    def form_valid(self, form):
        form.instance.lender = self.request.user
        return super().form_valid(form)

class TransactionDeleteView(LoginRequiredMixin,  DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    context_object_name = 'transaction'
    success_url = reverse_lazy('transaction_home')


