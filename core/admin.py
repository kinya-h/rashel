from django.contrib import admin
from .models import Customer, Category, Loan,Product, Game, Wallet, Transaction , Referral

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'date_created')
    list_per_page = 25
    ordering = ('-date_created',)
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_per_page = 25
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'referred_by' , 'created_at')
    list_per_page = 25
    ordering = ('user','referred_by' ,'created_at')
    search_fields = ('referred_by',)
    autocomplete_fields = ['referred_by']
    list_select_related = ['user']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('amount', 'duration' , 'customer' , "payment_status")
    list_per_page = 25
    ordering = ('amount','duration' ,'paid')
    search_fields = ('customer__first_name',)
    autocomplete_fields = ['customer']
    list_select_related = ['customer']


    def customer_first_name(self , loan):
        return loan.customer.first_name

    def customer_last_name(self , loan):
        return loan.customer.last_name

    @admin.display(ordering='paid')
    def payment_status(self, loan):
        if loan.paid == False:
            return 'Not Paid'
        return 'Paid'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'price')
    list_per_page = 25
    ordering = ('-id',)
    list_editable =['price']
    search_fields = ('title', 'description', 'category__name')
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }

    list_select_related = ['category']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'amount', 'date_created')
    list_per_page = 25
    ordering = ('-date_created',)
    search_fields = ('customer__first_name', 'customer__last_name', 'product__title')

    list_select_related = ['product']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('customer_fname', 'balance')
    list_per_page = 25
    ordering = ('-balance',)
    search_fields = ('customer_fname', 'customer_lname')

    
    
    list_select_related = ['customer']
    def customer_fname(self , wallet):
        return wallet.customer.first_name


    def customer_lname(self , wallet):
        return wallet.customer.last_name

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'date_created')
    list_per_page = 25
    ordering = ('-date_created',)
    search_fields = ('wallet__customer__first_name', 'wallet__customer__last_name')
