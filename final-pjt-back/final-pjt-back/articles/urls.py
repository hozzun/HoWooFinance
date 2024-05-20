from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    # 게시글 목록
    path('', views.article_list, name='article_list'),
    # 해당 게시글 조회
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    # 댓글 목록
    path('comments/', views.comment_list, name='comment_list'),
    # 댓글 생성
    path('<int:article_pk>/create/', views.comment_create, name='comment_create'),
    # 해당 댓글 조회
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]