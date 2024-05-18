from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, UserDetailsView
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, UserDetailInfoSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# 사용자 등록(회원가입) 뷰
class UserRegisterView(RegisterView):
    serializer_class = UserRegisterSerializer


# 사용자 로그인 뷰
class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer


# 사용자 정보 조회 뷰
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


# 회원정보 업데이트(변경) 뷰
class UserDetailInfoView(UserDetailsView):
    serializer_class = UserDetailInfoSerializer
    
    # 전체 업데이트
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    # 부분 업데이트
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    # 기존 데이터 가져와서 유효성 검사 후 업데이트 데이터 반환
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # 기존 데이터와 요청 데이터 사용하여 시리얼라이저 초기화
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 업데이트 데이터 저장
    def perform_update(self, serializer):
        serializer.save()