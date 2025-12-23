from django.shortcuts import render
from rest_framework import permissions, status,views,response
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post
from .models import Repost
# Create your views here.



class RepostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        Repost.objects.get_or_create(
            user=request.user,
            original_post=post
        )

        return response.Response({'detail': 'Post reposted'}, status=201)
