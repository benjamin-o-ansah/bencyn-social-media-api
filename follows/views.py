# follows/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from follows.models import Follow

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if user_to_follow == request.user:
            return Response({'error': "You can't follow yourself"}, status=400)
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        return Response({'message': 'User followed'}, status=201)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        Follow.objects.filter(follower=request.user, following_id=user_id).delete()
        return Response({'message': 'User unfollowed'}, status=200)
