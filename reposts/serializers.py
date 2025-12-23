from rest_framework import serializers
from .models import Repost


class RepostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    original_post = serializers.IntegerField(source='original_post.id', read_only=True)

    class Meta:
        model = Repost
        fields = [
            'id',
            'user',
            'original_post',
            'created_at',
        ]
