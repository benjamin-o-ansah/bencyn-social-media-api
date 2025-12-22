from django.shortcuts import render
from users.models import Follow
from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following_id", flat=True)
        queryset = Post.objects.filter(author_id__in=following_ids)
        # Optional filtering by ?search=keyword
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(content__icontains=search)
        # Optional filtering by ?date=YYYY-MM-DD
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(created_at__date=date)
        return queryset.select_related('author')

        return Post.objects.filter(
            author_id__in=following_ids
        ).select_related("author")