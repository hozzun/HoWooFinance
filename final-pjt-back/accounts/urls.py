from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserDetailInfoView, user_info

app_name = 'articles'
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
]