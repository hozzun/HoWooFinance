from django.urls import path
from . import views

app_name = 'deposits'
urlpatterns = [
    # 정기예금 상품 DB에 저장
    path('save_products/', views.save_deposit_products, name='save_products'),
    # 정기예금 상품옵션 DB에 저장
    path('save_options/', views.save_deposit_options, name='save_options'),
    # 전체 상품목록 조회 & 데이터 추가
    path('products/', views.deposit_products, name='deposit_products'),
    # 해당 상품 옵션 조회
    path('products/<str:fin_prdt_cd>/', views.deposit_detail, name='deposit_detail'),
]