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
    CHOICES = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )

    RENEWAL = (
        ('first time', 'first time'),
        ('second time', 'second time'),
        ('third time', 'third time'),
        ('fourth time', 'fourth time'),
        ('fifth time', 'fifth time'),
        
    )
    clients_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    amount_applied = models.IntegerField(default=0)
    amount_payable = models.IntegerField(default=0)
    defaulted_days = models.IntegerField(default=0)
    repayment = models.IntegerField(default=0)
    loan_disbursed = models.IntegerField(default=0)
    loan_repaid = models.IntegerField(default=0)
    fines_charged = models.IntegerField(default=0)
    transaction_fines = models.IntegerField(default=0)
    repayment_day = models.CharField(max_length=10, choices=CHOICES)
    renewal_time=models.CharField(max_length=200,choices=RENEWAL,blank=True)
    agreed_shedule = models.CharField(max_length=30, default='weekly')
    physical_address = models.CharField(max_length=50)
    security_offered = models.CharField(max_length=200, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)
    interest_rate = 0.3
   

    def __str__(self):
        return self.clients_name

    # =======absolute urls================#
    def get_absolute_url(self):
        return reverse('transaction_home')

    @property
    def interest_due(self):

        interest_charge = round(self.amount_applied *
                                self.interest_rate)+self.fines_charged
        return interest_charge

    @property
    def loan_payable_amount(self):
        method = self.interest_due
        return method+self.amount_applied

    @property
    def loan_balance_calculation(self):
        
        balance = self.amount_payable - self.repayment
        return balance
       

    @property
    def due_weekly_date(self):
        if self.agreed_shedule == "weekly":
            date = self.transaction_date
            due_date = date + relativedelta(weeks=+1)
            return due_date

    @property
    def loan_status(self):
        method = self.loan_balance_calculation
        method2 = self.interest_due
        if self.repayment > 0 and method == 0 and self.physical_address!='reset':
            return "cleared"
        elif self.repayment == method2 and self.physical_address!='reset':
            return "renewed interest for " + self.renewal_time
        elif self.physical_address == 'reset' and self.interest_due==0:
            return 'reset the system'    
        else:
            return "pending"
       

    

    @property
    def fines_calculation(self):
        if self.fines_charged == 0:
            method = self.interest_due
            return round(method / 7 * self.defaulted_days)
        else:
            return self.fines_charged

    @property
    def the_date_today(self):
        now = datetime.now()
        return now


#  =======================totals========================
    @property
    def loans_disbursed_total(self):
        method = Transaction.objects.aggregate(total=Sum('loan_disbursed'))
        return method['total']
    
    @property
    def loans_repaid_total(self):
        method = Transaction.objects.aggregate(total=Sum('loan_repaid'))
        return method['total']
    
    @property
    def cash_today_total(self):
        method = self.loans_repaid_total
        method2 =self.loans_disbursed_total
        return method - method2
    



    @property
    def fines_total(self):
        method = Transaction.objects.aggregate(total=Sum('fines_charged'))
        return method['total']

    @property
    def interest_total(self):
        method1 = self.fines_total
        method2 = Transaction.objects.aggregate(total=Sum('amount_applied'))
        return round(method2['total'] * self.interest_rate) + method1

    @property
    def loans_given_total(self):
        method2 = Transaction.objects.aggregate(total=Sum('amount_applied'))
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

    @property
    def loan_balance_total(self):
        method1 = self.repayments_total
        method2 = Transaction.objects.aggregate(total=Sum('amount_payable'))
        return method2['total'] - method1



class Cylinder(models.Model):
    CHOICES = (
        ('13kg', '13kg'),
        ('6kg', '6kg'),
        ('3kg', '3kg'),
        ('reset','reset'),
    )

    TRANSACTION = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )
    cylinder_capacity = models.CharField(max_length=100, choices=CHOICES)
    transaction_day = models.CharField(max_length=100, choices=TRANSACTION,default=None)
    item = models.CharField(max_length=20, default='cylinder')
    total_cylinders = models.IntegerField(default=0)
    cylinders_taken_for_refilling = models.IntegerField(default=0)
    exchange_price = models.IntegerField(default=0)
    cylinders_exchanged = models.IntegerField(default=0)
    total_cylinder_sales = models.IntegerField(default=0)
    other_accessories = models.IntegerField(default=0)
    burners = models.IntegerField(default=0)
    grills = models.IntegerField(default=0)
    transaction_date = models.DateTimeField('date published', auto_now=True)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.item

    def get_absolute_url(self):
        return reverse('cylinder_home')

    def remaining_cylinders(self):
        return self.total_cylinders-self.cylinders_taken_for_refilling

    def collection_for_the_day(self):
        return self.cylinders_exchanged * self.exchange_price
    
    def sales_total(self):
        method = Cylinder.objects.aggregate(total=Sum('total_cylinder_sales'))
        return method['total']
    
    def burners_total(self):
        method = Cylinder.objects.aggregate(total=Sum('burners'))
        return method['total']
    
    def grills_total(self):
        method = Cylinder.objects.aggregate(total=Sum('grills'))
        return method['total']
    
    def accessories_total(self):
        method = Cylinder.objects.aggregate(total=Sum('other_accessories'))
        return method['total']



class Sale(models.Model):
    CHOICES = (
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
        ('saturday', 'saturday'),
        ('sunday', 'sunday'),
    )
    sales_day = models.CharField(max_length=100, choices=CHOICES)
    todays_sale = models.CharField(max_length=200, default='add sales')
    cylinder_sales = models.IntegerField(default=0)
    electronics_and_accessories_sales = models.IntegerField(default=0)
    loans_disbursed = models.IntegerField(default=0)
    loans_repaid = models.IntegerField(default=0)
    transaction_date = models.DateTimeField('date published', auto_now=True)
    lender = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.todays_sale

    def get_absolute_url(self):
        return reverse('sales_home')

    def total_revenue(self):
        return self.cylinder_sales+self.electronics_and_accessories_sales+self.loans_repaid-self.loans_disbursed
