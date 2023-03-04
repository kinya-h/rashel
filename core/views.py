import requests
import base64
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin,UpdateModelMixin
from django.db.models import Sum,Avg,Max,Min,Count,F,Q
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Customer, Category, Product, Game, Wallet, Transaction , Loan,Referral
from .serializers import CustomerSerializer, CategorySerializer, ProductSerializer, GameSerializer, WalletSerializer, TransactionSerializer , LoanSerializer,ReferralSerializer
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from datetime import datetime
from .mpesa_auth import get_acess_token

from django_nextjs.render import render_nextjs_page_sync
def index(request):
    return render_nextjs_page_sync(request)



class ReactAppView(TemplateView):
    template_name = 'index.html'

class LoginViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print("User = " , user  )
        print("username" , username)
        print("password" , password)
        if user is not None:
            login(request, user)
            return Response({'authenticated': True})
        else:
            return Response({'authenticated': False})

    def list(self, request, *args, **kwargs):
        return Response({'detail': 'Method "GET" not allowed.'}, status=405)

    def retrieve(self, request, *args, **kwargs):
        return Response({'detail': 'Method "GET" not allowed.'}, status=405)

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PUT" not allowed.'}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PATCH" not allowed.'}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Method "DELETE" not allowed.'}, status=405)



class CustomerViewSet(CreateModelMixin , RetrieveModelMixin , UpdateModelMixin , GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    # @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    # def history(self, request, pk):
    #     return Response('ok')

    def create(self, request, *args, **kwargs):
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
       
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer


    
    def delete(self , request , pk):
        category = get_object_or_404(Category , pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'This Collection cannot be deleted'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id']


    
    def get_serializer_context(self):
        return {'request':self.request} 
        
class ReferralViewSet(ModelViewSet):

    queryset = Referral.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReferralSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['referrer']


    def create(self, request, *args, **kwargs):
        (referral, created) = Referral.objects.get_or_create(
            user_id=request.user.id)
        serializer = ReferralSerializer(referral, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer_id']
    permission_classes = [IsAdminUser]



    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def request(self, request):
        (loan, created) = Loan.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = LoanSerializer(loan, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = LoanSerializer(loan, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        (wallet, created) = Wallet.objects.get_or_create(
            customer_id=request.user.id)
       
        serializer = WalletSerializer(wallet, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (wallet, created) = Wallet.objects.get_or_create(
            customer_id=request.user.id)
        if request.method == 'GET':
            serializer = WalletSerializer(wallet)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = WalletSerializer(wallet, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# class TransactionViewSet(ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

class STKPushViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer 
    

    @action(detail=False, methods=['post'])
    def push(self, request):
        transaction_data = request.data
        print("Transaction data = " , transaction_data)
    # Set the access token
        access_token = get_acess_token()['access_token']
        shortcode = ''
        passkey = ''
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # "BusinessShortCode": 174379,
    #     "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMjI0MjIzMzU1",
    #     "Timestamp": "20230224223355",
    #     "TransactionType": "CustomerPayBillOnline",
    #     "Amount": ,
    #     "PartyA": 254708374149,
    #     "PartyB": 174379,
    #     "PhoneNumber": 254708374149,
        # amount = request.data.amount
        # password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()
        password = "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMjI0MjIzMzU1"


        # Set the Safaricom STK push API endpoint
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        # Set the request headers
        headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
        PhoneNumber = request.data.get('phone')
        PhoneNumber = PhoneNumber.replace(PhoneNumber[0], '4', 1)
        phone_initial = '25' 
        PhoneNumber = phone_initial + PhoneNumber 
        # Set the request body
        payload = {
            "BusinessShortCode": "174379",
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMjI0MjI0ODA2",
            "Timestamp": "20230224224806",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(transaction_data.get('amount')),
            "PartyA": int(PhoneNumber),
            "PartyB": "174379",
            "PhoneNumber": int(PhoneNumber),
            # "CallBackURL": "https://rashel-production.up.railway.app/api/stk-push-callback/callback_url",
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X"
        }

        # Send the request
        response = requests.post(url, json=payload, headers=headers)

        # Print the response
        print(response.text)
        return Response(response.text)

class STKPushCallbackViewSet(ModelViewSet):
    """
    A viewset that handles the callback URL for Safaricom STK push requests.
    """
    
    @action(detail=False, methods=['post'])
    def callback_url(self, request):
        # Parse the response data
        data = request.data
        
        # Check if the transaction was successful
        if data['Body']['stkCallback']['ResultCode'] == 0:
            # Get the transaction details
            transaction = data['Body']['stkCallback']['CallbackMetadata']['Item']
            
            # Extract the relevant fields
            amount = transaction[0]['Value']
            mpesa_receipt_number = transaction[1]['Value']
            transaction_date_str = transaction[3]['Value']
            transaction_date = datetime.strptime(transaction_date_str, '%Y%m%d%H%M%S')
            print("Transaction Status = " , transaction)
            # Do something with the transaction details, such as updating your database
            # ...
            
            # Return a success response
            return Response({'ResultCode': 0, 'ResultDesc': 'The service was accepted successfully'})
        else:
            # Return an error response
            return Response({'ResultCode': 1, 'ResultDesc': 'The service was not accepted'}, status=400)    
