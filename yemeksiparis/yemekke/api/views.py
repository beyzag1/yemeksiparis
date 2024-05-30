from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets
from rest_framework.generics import get_object_or_404
from yemekke.models import User, ProductCategory, Order, Product,SellerUser,OrderItem,UserProfile
from yemekke.api.permissions import IsRestaurantOwnerOrReadOnly, IsOwnerOrReadOnly
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView 

from yemekke.api.serializers import (
    UserProfileSerializer,
    UserRegisterSerializer,
    SellerUserProfileSerializer,
    ProductCategorySerializer,
    SellerUserSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderItemSerializer,
    SellerRegisterSerializer
   
)
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView

class UserProfileAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



class SellerProfileAPIView(generics.ListCreateAPIView):
    queryset = SellerUser.objects.all()
    serializer_class = SellerUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class SellerUserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SellerUser.objects.all()
    serializer_class = SellerUserSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly ]  

class ProductCategoryAPIView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        category = serializer.validated_data.get('category')
        restaurant = self.request.user.restaurantprofile  
        serializer.save(category=category, restaurant=restaurant) 


class ProductCategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    

class SellerUserAPIView(APIView):
    def get(self, request):
        users = SellerUser.objects.all()
        serializer = SellerUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SellerUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = SellerUser.objects.get(pk=pk)
        serializer = SellerUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = SellerUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

class OrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        print(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        adress = request.data.get('adres')
        telefon = request.data.get('telefon')
        
        if User.objects.filter(username__iexact=username).exists():
            print("deneme123")
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email__iexact=email).exists():
            print("deneme223")
            return JsonResponse({'error': 'Email already exists'}, status=400)
        if password1 != password2:
            print("deneme333")
            return JsonResponse({'error': "Passwords don't match"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)

        customer_profile = UserProfile.objects.create(user=user, telefon=telefon, adress=adress)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class SellerRegisterView(RegisterView):
    serializer_class = SellerRegisterSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        name = request.data.get('name')
        address = request.data.get('address')
        image = request.data.get('image')
        minimum_order_amount = request.data.get('minimum_order_amount')
        categories = request.data.getlist('categories')  
        print(request.data["categories"])
        if User.objects.filter(username__iexact=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=401)
        if User.objects.filter(email__iexact=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=402)
        if password1 != password2:
            return JsonResponse({'error': "Passwords don't match"}, status=403)

        user = User.objects.create_user(username=username, email=email, password=password1)
        SellerUser_profile = SellerUser.objects.create(
            user=user,
            name=name,
            address=address,
            image=image,
            minimum_order_amount=minimum_order_amount
        )
        SellerUser_profile.categories.set(categories)  

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


     