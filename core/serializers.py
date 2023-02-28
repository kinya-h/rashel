from rest_framework import serializers
from .models import Customer, Category, Product, Game, Wallet, Transaction, Loan

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id' , 'user_id' , "phone" , 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Game
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Wallet
        fields = '__all__'
class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = ['amount' , 'duration' , 'paid', 'customer']
class TransactionSerializer(serializers.ModelSerializer):
    
    wallet = WalletSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'
