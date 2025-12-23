from django.shortcuts import render
from rest_framework import viewsets, permissions,response,status
from follows.models import Follow
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
        # following_ids = Follow.objects.filter(
        #     follower=self.request.user
        # ).values_list("following_id", flat=True)
        # queryset = Post.objects.filter(author_id__in=following_ids)
        # # Optional filtering by ?search=keyword
        # search = self.request.query_params.get('search')
        # if search:
        #     queryset = queryset.filter(content__icontains=search)
        # # Optional filtering by ?date=YYYY-MM-DD
        # date = self.request.query_params.get('date')
        # if date:
        #     queryset = queryset.filter(created_at__date=date)
        #     return queryset.select_related('author')
        
        # return Post.objects.filter(
        #     author_id__in=following_ids).select_related("author")
        following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following_id", flat=True)

        queryset = Post.objects.filter(author_id__in=following_ids)

        # Optional search filter
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(content__icontains=search)

        # Optional date filter
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(created_at__date=date)

        # return queryset.select_related("author").prefetch_related("comments", "likes")
        return Post.objects.filter(author_id__in=following_ids)\
            .select_related("author")\
            .prefetch_related("comments", "likes")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return response.Response(
            {
                "status": "success",
                "message": "Feed retrieved successfully",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )