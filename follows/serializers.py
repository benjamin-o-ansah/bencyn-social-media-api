from rest_framework import serializers
from follows.models import Follow
from django.contrib.auth.models import User
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['follower']
    
    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs.get('following')
        if user == following:
            raise serializers.ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(follower=user, following=following).exists():
            raise serializers.ValidationError("You are already following this user.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        following = validated_data['following']
        follow_instance = Follow.objects.create(follower=user, following=following)
        return follow_instance

class UserFollowStatsSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'followers_count', 'following_count']

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()