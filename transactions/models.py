# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import calendar

# ===========transactions=============================


class Transaction(models.Model):
    clients_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    loan_given = models.IntegerField(default=0)
    loan_balance=models.IntegerField(default=0)
    defaulted_days = models.IntegerField(default=0)
    repayment = models.IntegerField(default=0)
    weekly_shedule = models.IntegerField(default=0)
    fines =models.IntegerField(default=0)
    transaction_fines =models.IntegerField(default=0)
    weekly_due_day = models.CharField(max_length=200)
    monthly_due_date = models.DateTimeField(default=timezone.now)
    agreed_shedule=models.CharField(max_length=30)
    residence = models.CharField(max_length=50)
    loan_collateral = models.CharField(max_length=200)
    transaction_date=models.DateTimeField('date published', auto_now=True)
    lender=models.ForeignKey(User,on_delete=models.CASCADE)
    interest_rate = 0.3
    penalty=0.05

    
    
    
    def __str__(self):
        return self.clients_name

    # =======absolute urls================#
    def get_absolute_url(self):
        return reverse('transaction_home')
   
    @property
    def interest_due(self):
        
        interest_charge = round(self.loan_given * self.interest_rate)+self.fines
        return interest_charge
    
    @property
    def loan_payable_amount(self):
        method = self.interest_due
        return method+self.loan_given
         
        
       
    @property
    def installments(self):
        if self.agreed_shedule=="weekly":
            method = self.loan_payable_amount
            return method / 4
        else:
            return 0

    @property
    def loan_balance_calculation(self):
        balance = self.loan_balance - self.repayment
        return balance

    
    @property
    def due_month_date(self):
        if self.agreed_shedule=="monthly":
            date = datetime.now()
            due_date = date + relativedelta(months=+1)
            return due_date
    
    @property
    def due_weekly_day(self):
        if self.agreed_shedule == "weekly":
            return datetime.today().strftime('%A')
        else:
            return ""
   

  
#  =======================totals========================
    
    @property
    def fines_total(self):
       method = Transaction.objects.aggregate(total=Sum('fines'))
       return method['total']
            
    @property
    def interest_total(self):
        method1=self.fines_total
        method2=Transaction.objects.aggregate(total=Sum('loan_given'))
        return round(method2['total'] * self.interest_rate) +method1
    
    @property
    def loans_given_total(self):
        method2 = Transaction.objects.aggregate(total=Sum('loan_given'))
        return method2['total']
    
    @property
    def loans_payable_total(self):
        method1 = self.interest_total
        method2 = self.loans_given_total
        return method1+method2

    @property
    def repayments_total(self):
        method2 = Transaction.objects.aggregate(total=Sum('repayment'))
        return method2['total']
        

    
   
'''
    @property
    def defaulted_days_total(self):
       method = Transaction.objects.aggregate(total=Sum('defaulted_days'))
       return method['total']

    @property
    def cash_total(self):
        method=Transaction.objects.aggregate(total=Sum('cash_repayment'))
        return method['total']

    
        
    @property
    def loans_total(self):
        method1 = self.interest_total
        method3 = self.cash_total
        method4 = self.mpesa_total
        
        method2 = Transaction.objects.aggregate(total=Sum('loan_given')) 
        
        return method2['total']+method1 -(method3+method4 )  

        '''