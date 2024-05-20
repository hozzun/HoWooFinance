from rest_framework import serializers
from .models import Article, Comment

# 게시글 전체 목록 시리얼라이저
class ArticleListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', )


# 댓글 시리얼 라이저
class CommentSerializer(serializers.ModelSerializer):
    article_id = serializers.ReadOnlyField(source='article.id')
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = ('id', 'username', 'content', 'created_at', 'updated_at', 'article_id', 'user_id', )


# 게시글 시리얼라이저
class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', )