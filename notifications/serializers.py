from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'actor',
            'verb',
            'target_id',
            'is_read',
            'created_at',
        ]
        read_only_fields = [
            'actor',
            'verb',
            'target_id',
            'created_at',
        ]
