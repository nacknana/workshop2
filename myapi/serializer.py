from itertools import product
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ParseError, ValidationError

from django.contrib.auth.models import User

from datetime import datetime

from .models import Cart, Category, ImgsProduct, Product


def get_current_date(sec):
    # print()
    return datetime.fromtimestamp(datetime.timestamp(datetime.now())+int(sec)).strftime("%d/%m/%Y, %H:%M:%S")


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # print('attrs  ==>> ', attrs)
        try:
            data = super().validate(attrs)
            token = self.get_token(self.user)

            # data['access_token'] = str(token.access_token)
            data['token_type'] = str(token.access_token.token_type)
            data['expire_in'] = get_current_date(
                token.access_token.lifetime.total_seconds())
            # data['refresh_token'] = str(token)
            # print('token ==>>>', data)
            return data
        except:
            raise ParseError(
                {'msg': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'code': 'LOGIN_FAIL'})


class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        # try:
        data = super().validate(attrs)
        # if data:
        # print('data >= ', type(data))
        refresh = RefreshToken(attrs['refresh'])
        data['token_type'] = str(refresh.token_type)
        data['expire_id'] = get_current_date(
            refresh.access_token.lifetime.total_seconds())

        data['refresh_token'] = str(refresh)
        # print(data)
        return data
    # else:
        # print('No Refresh token')

        # raise RefreshTokenError()

        # except:
        # raise ParseError({'msg': 'Login Fail'})


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, error_messages={
        "blank": "ชื่อผู้ใช้เป็นค่าว่าง กรุณากรอกชื่อผู้ใช้"})
    password = serializers.CharField(max_length=20, error_messages={
        "blank": "รหัสผ่านเป็นค่าว่าง กรุณากรอกรหัสผ่าน"})

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',  'last_name')

    def validate_password(self, password):
        if password is None:
            raise ValidationError('กรุณาใส่รหัสผ่าน')
        if len(password) < 8:
            raise ValidationError('รหัสผ่านน้อยกว่า 8 ตัว')
        return password

    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError('มีชื่อผู้ใช้นี้แล้ว')
        return username

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'img', 'name', 'enable', 'detail']


class ProductImgs(serializers.ModelSerializer):
    class Meta:
        model = ImgsProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # imgs_product = ProductImgs(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'img', 'name', 'enable', 'detail', 'products']


class ProductDetailSerializer(serializers.ModelSerializer):
    imgs_product = ProductImgs(many=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price',
                  'img', 'enable', 'imgs_product']

    # def get_category(self, obj):
    #     return obj.category.name


class CartSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(error_messages={
        "blank": 'ระบุรหัสสินค้า', 'write_only': True
    })
    quantity = serializers.IntegerField(error_messages={
        "blank": "ระบุจำนวนสินค้า", 'write_only': True
    })

    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise ValidationError('จำนวนสินค้าต้องมากกว่า 0 ชิ้น')
        return quantity

    def validate_product(self, product):
        # print(type(product))
        try:
            prod = Product.objects.get(pk=product)
        except:
            raise ValidationError('ไม่พบสินค้านี้')
        if not prod.enable:
            raise ValidationError('สินค้าถูกปิดใช้งาน')
        return product

    class Meta:
        model = Cart
        fields = ['product',  'quantity']


class CartUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(error_messages={
        "blank": "ระบุจำนวนสินค้า", 'write_only': True
    })

    def validate_quantity(self, quantity):
        if quantity < 0:
            return 0
        return quantity

    class Meta:
        model = Cart
        fields = ['quantity']


class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'product',  'quantity',  'total']
