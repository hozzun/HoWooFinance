from dj_rest_auth.registration.views import RegisterView, LoginView
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response


# Create your views here.

# 사용자 등록 뷰
class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer

# 사용자 로그인 뷰
class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer

# 사용자 정보 조회 뷰
@api_view(['GET'])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)