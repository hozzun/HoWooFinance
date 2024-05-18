import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer

# Create your views here.
API_KEY = settings.API_KEY_DEPOSIT
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'


# 예금상품 DB에 저장
@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    context = {
        'auth': API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1,
    }
    response = requests.get(URL, params=context).json()

    # 상품
    for pli in response.get('result').get('baseList'):
        fin_prdt_cd = pli.get('fin_prdt_cd')
        fin_prdt_nm = pli.get('fin_prdt_nm')
        kor_co_nm = pli.get('kor_co_nm')
        mtrt_int = pli.get('mtrt_int')
        spcl_cnd = pli.get('spcl_cnd')
        join_way = pli.get('join_way')
        join_deny = pli.get('join_deny')
        join_member = pli.get('join_member')
        etc_note = pli.get('etc_note')

        save_product_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'fin_prdt_nm': fin_prdt_nm,
            'kor_co_nm': kor_co_nm,
            'mtrt_int': mtrt_int,
            'spcl_cnd': spcl_cnd,
            'join_way': join_way,
            'join_deny': join_deny,
            'join_member': join_member,
            'etc_note': etc_note,
        }

        product_serializer = DepositProductsSerializer(data=save_product_data)
        if product_serializer.is_valid(raise_exception=True):
            product_serializer.save()
    
    # 옵션
    for oli in response.get('result').get('optionList'):
        fin_prdt_cd = oli.get('fin_prdt_cd')
        intr_rate_type_nm = oli.get('intr_rate_type_nm')
        save_trm = oli.get('save_trm')
        intr_rate = oli.get('intr_rate')
        intr_rate2 = oli.get('intr_rate2')

        save_option_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': intr_rate_type_nm,
            'save_trm': save_trm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
        }

        fin_prdt_cd = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        print(fin_prdt_cd)
        option_serializer = DepositOptionsSerializer(data=save_option_data)
        if option_serializer.is_valid(raise_exception=True):
            option_serializer.save(fin_prdt_cd=fin_prdt_cd)
    
    return JsonResponse({ "message": "okay" })


# 상품 목록 조회 및 추가
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


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    
    return Response(serializer.data)
