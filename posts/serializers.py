# posts/serializers.py
from rest_framework import serializers
from .models import Post
# from interactions.models import Comment
from interactions.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    latest_comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    latest_comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "media_url",
            "created_at",
            "updated_at",
            "latest_comments",    # Include comments in the list
            "likes_count"
        ]
        read_only_fields = ["author", "created_at"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value


    def get_latest_comments(self, obj):
        # obj is the Post instance
        comments = obj.comments.all().order_by('-created_at')[:3]
        return CommentSerializer(comments, many=True).data