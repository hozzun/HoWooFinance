from django.urls import path
from . import views

app_name = 'savings'
urlpatterns = [
    # 적금 상품 DB에 저장
    path('save_products/', views.save_saving_products, name='save_products'),
    # 적금 상품옵션 DB에 저장
    path('save_options/', views.save_saving_options, name='save_options'),
    # 전체 상품목록 조회 & 데이터 추가
    path('products/', views.saving_products, name='saving_products'),
    # 해당 상품 옵션 조회
    path('products/<str:fin_prdt_cd>/', views.saving_detail, name='saving_detail'),
]