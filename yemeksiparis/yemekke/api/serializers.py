from dj_rest_auth.registration.serializers import RegisterSerializer 
from rest_framework import serializers
from yemekke.models import User,Product,ProductCategory,SellerUser,Order,OrderItem
from django.contrib.auth.models import User


class UserRegisterSerializer(RegisterSerializer):
    adres = serializers.CharField()
    telefon = serializers.CharField()

    def custom_signup(self, request, user):
        user.save()

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        return data_dict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields='__all__'

    def get_user(self,obj):
        return obj.user.username if obj.user else None  

class SellerUserProfileSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = SellerUser
        fields = ['id','products','name','adress','image','minimum_order_amount','user','categories']  


    def get_categories(self,obj):
        return[category.name for category in obj.categories.all()] 


    def get_products(self, obj):
        products = Product.objects.filter(restaurant=obj)
        product_data = []
        for product in products:
            product_data.append({
                'name': product.name,
                'description': product.description,
                'price': product.price,
                # 'image': product.image,
                'category': product.category.name,
                'image': product.image.url
            })
        return product_data  

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'    

class SellerUserSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SellerUser
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    restoran = SellerUserSerializer(read_only=True)
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    restaurant = SellerUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'additional_notes', 'price']



class SellerRegisterSerializer(RegisterSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    address = serializers.CharField()
    image = serializers.ImageField()
    minimum_order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'address', 'image', 'minimum_order_amount', 'category']

    def create(self, validated_data):
        user_data = {key: validated_data.pop(key) for key in ['username', 'password', 'email']}
        user = User.objects.create_user(**user_data)
        SellerUser.objects.create(user=user, **validated_data)
        return user
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'additional_notes', 'price']

