from django.urls import path
from . import views

app_name = 'deposits'
urlpatterns = [
    # 예금상품 DB에 저장
    path('save/', views.save_deposit_products, name='save_products'),
    # 상품목록 출력 & 데이터 추가
    path('products/', views.deposit_products, name='products_data'),
    # 특정 상품 옵션 조회
    path('products/<str:fin_prdt_cd>/', views.deposit_product_options),
]