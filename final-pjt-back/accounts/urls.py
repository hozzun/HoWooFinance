from django.urls import path, include
from .views import UserRegisterView, UserLoginView, user_info

app_name = 'articles'
urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', UserRegisterView.as_view(), name='account_signup'),
    path('user/', user_info, name='user_info'),
    path('login/', UserLoginView.as_view(), name='account_login')
]