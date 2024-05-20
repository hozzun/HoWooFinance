from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserDetailInfoView, user_info, add_to_deposit, remove_from_deposit, add_to_saving, remove_from_saving

app_name = 'accounts'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    # 회원 가입
    path('signup/', UserRegisterView.as_view(), name='account_signup'),
    # 로그인
    path('login/', UserLoginView.as_view(), name='account_login'),
    # 회원 정보(업데이트)
    path('update/', UserDetailInfoView.as_view(), name='account_update'),
    # 회원 정보(조회)
    path('user_info/', user_info, name='user_info'),
    # 정기예금 가입
    path('deposit/add/', add_to_deposit, name='add_deposit'),
    # 정기예금 가입취소
    path('deposit/remove/', remove_from_deposit, name='remove_deposit'),
    # 적금 가입
    path('saving/add/', add_to_saving, name='add_saving'),
    # 적금 가입취소
    path('saving/remove/', remove_from_saving, name='remove_saving'),
]