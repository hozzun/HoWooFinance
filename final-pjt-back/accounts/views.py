from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, UserDetailsView
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, UserDetailInfoSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from deposits.models import DepositProducts, DepositOptions
from savings.models import SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, SavingProductsSerializer
from deposits.serializers import DepositOptionsSerializer
from savings.serializers import SavingOptionsSerializer
from django.db import transaction
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        logger.debug(f"User registration data: {request.data}")
        return super().create(request, *args, **kwargs)


class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserDetailInfoView(UserDetailsView):
    serializer_class = UserDetailInfoSerializer
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        if not serializer.is_valid():
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_deposit(request):
    user = request.user
    
    product_code = request.data.get('product_code')
    product_trm = request.data.get('product_trm')

    if not all([product_code, product_trm]):
        return Response({'error': '모든 필드를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product_trm = int(product_trm)
    except ValueError:
        return Response({'error': '유효한 product_trm 값을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = DepositProducts.objects.get(fin_prdt_cd=product_code)
    except DepositProducts.DoesNotExist:
        return Response({'error': '유효한 제품 코드가 아닙니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    options = DepositOptions.objects.filter(fin_prdt_cd=product, save_trm=product_trm)
    
    if not options.exists():
        return Response({'error': '유효한 저축 기간이 아닙니다.'}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        user.deposit.add(product)
        for option in options:
            option.users.add(user)

    return Response({'message': '정기예금 가입이 완료되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_deposit(request):
    user = request.user
    product_code = request.data.get('product_code')

    product = get_object_or_404(DepositProducts, fin_prdt_cd=product_code)
    user.deposit.remove(product)

    # 삭제 후 해당 사용자의 관련 옵션도 제거
    options = DepositOptions.objects.filter(fin_prdt_cd=product, users=user)
    for option in options:
        option.users.remove(user)

    return Response({'message': '정기예금 가입 취소가 완료되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_saving(request):
    user = request.user
    
    product_code = request.data.get('product_code')
    product_trm = request.data.get('product_trm')

    if not all([product_code, product_trm]):
        return Response({'error': '모든 필드를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product_trm = int(product_trm)
    except ValueError:
        return Response({'error': '유효한 product_trm 값을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = SavingProducts.objects.get(fin_prdt_cd=product_code)
    except SavingProducts.DoesNotExist:
        return Response({'error': '유효한 제품 코드가 아닙니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    options = SavingOptions.objects.filter(fin_prdt_cd=product, save_trm=product_trm)
    
    if not options.exists():
        return Response({'error': '유효한 저축 기간이 아닙니다.'}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():
        user.saving.add(product)
        for option in options:
            option.users.add(user)

    return Response({'message': '적금 가입이 완료되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_saving(request):
    user = request.user
    product_code = request.data.get('product_code')

    product = get_object_or_404(SavingProducts, fin_prdt_cd=product_code)
    user.saving.remove(product)

    # 삭제 후 해당 사용자의 관련 옵션도 제거
    options = SavingOptions.objects.filter(fin_prdt_cd=product, users=user)
    for option in options:
        option.users.remove(user)

    return Response({'message': '정기예금 가입 취소가 완료되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_deposit_products(request):
    user = request.user
    deposit_products = user.deposit.all()
    result = []
    for product in deposit_products:
        options = product.depositoptions_set.filter(users=user)
        product_data = DepositProductsSerializer(product, context={'request': request}).data
        product_data['deposit_options'] = DepositOptionsSerializer(options, many=True).data
        result.append(product_data)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_saving_products(request):
    user = request.user
    saving_products = user.saving.all()
    result = []
    for product in saving_products:
        options = product.savingoptions_set.filter(users=user)
        product_data = SavingProductsSerializer(product, context={'request': request}).data
        product_data['saving_options'] = SavingOptionsSerializer(options, many=True).data
        result.append(product_data)
    return Response(result, status=status.HTTP_200_OK)

