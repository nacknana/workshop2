from django.contrib.auth.models import User

from rest_framework import permissions, generics, mixins, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# from .pagination import CustomPagination
from .serializer import *
from .models import Category


# Create your views here.


class RespondData():
    def __init__(self, user=None, *args, **kwargs):

        self.respond = {
            'msg': kwargs.get('msg', 'ดึงข้อมูลสำเร็จ'),
            'data':  kwargs.get('data', [])

        }


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class RefreshTokenView(TokenObtainPairView):
    serializer_class = RefreshTokenSerializer


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(request.data)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "token_type": str(refresh.token_type),
                    "refresh": str(refresh),
                    "expire_in":
                        get_current_date(
                        refresh.access_token.lifetime.total_seconds())
                },
                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterViewSet()
class CategoryGenericsView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['enable']

    def __init__(self, *args, **kwargs):
        self.response_format = RespondData().respond
        super(CategoryGenericsView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        response_data = super(CategoryGenericsView, self).list(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['status'] = True
        if not response_data.data:
            self.response_format['message'] = 'List Empty'
        return Response(self.response_format)


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        data = self.get_serializer(obj)
        return Response({
            'data': data.data
        }, status=status.HTTP_200_OK)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['enable']
    # pagination_class = CustomPagination

    def __init__(self, *args, **kwargs):
        self.response_data = RespondData().respond
        super(ProductListAPIView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = self.get_serializer(queryset, many=True).data

        if not data:
            self.response_data['message'] = 'List Empty'
        self.response_data['data'] = data
        return Response(self.response_data, status=status.HTTP_200_OK)


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filterset_fields = ['enable']

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        data = self.get_serializer(obj)
        return Response({
            'data': data.data
        }, status=status.HTTP_200_OK)


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialize = CartListSerializer(queryset, many=True)
        # print(queryset)
        print(serialize.data)
        res = RespondData().respond
        res['data'] = serialize.data
        # return Response({
        #     'err': 'Don\'t have Permision'
        # }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response(res)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            prod = Product.objects.get(pk=data['product'])
            user = request.user

            item = Cart.objects.filter(user=user, product=prod).first()
            # print(item.product)
            if item:
                new_qty = item.quantity = data['quantity'] + item.quantity
                item.total = item.product.price * new_qty
                item.save()
            else:
                item = Cart(
                    user=user,
                    product=prod,
                    quantity=data['quantity'],
                    total=data['quantity'] * prod.price)
                item.save()

            data['id'] = item.id
            data['product'] = item.product.name
            data['quantity'] = item.quantity
            data['total'] = item.total
            res = Response({
                'data': data,
                'msg': "บันทึกสำเร็จ",
            }, status=status.HTTP_201_CREATED)
        else:
            res = Response({
                "code": "ADD_TO_CART_FAIL",
                'msg': "บันทึกไม่สำเร็จ",
                "error": serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)
        return res


class CartUpdate(generics.UpdateAPIView):
    # queryset = Cart.objects.all()
    serializer_class = CartUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     return Response({
    #         "detail": "Method \"GET\" not allowed."
    #     }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data)
        # print(kwargs['pk'])
        # print(serialize)
        if serialize.is_valid():
            data = serialize.data

            user = request.user.id

            item = Cart.objects.filter(id=int(kwargs['pk']), user=user).first()

        #     # print(item.product)
            if item:
                new_qty = item.quantity = data['quantity']
                item.total = item.product.price * new_qty
                item.save()
                data['id'] = item.id
                data['product'] = item.product.name
                data['quantity'] = item.quantity
                data['total'] = item.total

                res = Response({
                    'msg': "บันทึกสำเร็จ",
                    'data': data
                }, status=status.HTTP_200_OK)

                if item.quantity == 0:
                    item.delete()
                    res = Response({
                        'msg': "ลบสำเร็จ",
                    }, status=status.HTTP_200_OK)

            else:
                res = Response({
                    "code": "HTTP_404_NOT_FOUND",
                    'msg': "ไม่พบข้อมูล",
                }, status=status.HTTP_404_NOT_FOUND)

        else:
            res = Response({
                "code": "ADD_TO_CART_FAIL",
                'msg': "บันทึกไม่สำเร็จ",
                "error": serialize.errors
            }, status=status.HTTP_401_UNAUTHORIZED)

        return res
        # super().get(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     return Response({
    #         'data': 'data'
    #     })


class CartDestroy(generics.DestroyAPIView):
    # serializer_class = CartListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = request.user

        cart_id = int(kwargs['cart_id'])
        product = int(kwargs['product_id'])
        cart = Cart.objects.filter(id=cart_id, product=product).first()
        if not cart:
            return Response({
                'code': 'HTTP_404_NOT_FOUND',
                'msg': 'ไม่พบข้อมูล'
            }, status=status.HTTP_404_NOT_FOUND)

        if cart.user != user:
            return Response({
                'code': 'HTTP_403_FORBIDDEN',
                'msg': 'ไม่มีสิทธ์เข้าใช้งาน',
            }, status=status.HTTP_403_FORBIDDEN)
        cart.delete()
        return Response({
            'msg': 'ลบสำเร็จ'
        }, status=status.HTTP_200_OK)

        # super().destroy(request, *args, **kwargs)
