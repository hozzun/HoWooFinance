import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
API_KEY = settings.API_KEY_DEPOSIT
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'


# 정기예금 상품 DB에 저장
@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    context = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=context).json()
    base_list = response['result']['baseList']

    # product
    for base in base_list:
        save_base_data = {
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_way': base.get('join_way'),
            'join_deny': base.get('join_deny'),
            'join_member': base.get('join_member'),
            'etc_note': base.get('etc_note'),
        }

        product_serializer = DepositProductsSerializer(data=save_base_data)
        if product_serializer.is_valid(raise_exception=True):
            product_serializer.save()

    return JsonResponse({"message": "정기예금 상품 저장완료."}) 


# 정기예금 상품옵션 DB에 저장
@api_view(['GET'])
def save_deposit_options(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    context = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=context).json()
    option_list = response['result']['optionList']
    
    # option
    for option in option_list:
        fin_prdt_cd = option.get('fin_prdt_cd')

        # 해당 상품이 존재하는지 확인
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        except DepositProducts.DoesNotExist:
            continue
        
        save_option_data = {
            'intr_rate_type_nm': option.get('intr_rate_type_nm'),
            'intr_rate': option.get('intr_rate'),
            'intr_rate2': option.get('intr_rate2'),
            'save_trm': option.get('save_trm'),
        }

        option_serializer = DepositOptionsSerializer(data=save_option_data)
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(fin_prdt_cd=product)

    return JsonResponse({"message": "정기예금 옵션 저장완료."}) 


# (정기예금)전체 상품 목록 조회 및 추가
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'})


# (정기예금)해당 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_detail(request, fin_prdt_cd):
    product = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    options = DepositOptions.objects.filter(fin_prdt_cd=product)
    serializer = DepositOptionsSerializer(options, many=True)
    
    return Response(serializer.data)