from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from .models import Like, Comment
from .serializers import CommentSerializer


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = generics.get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {'detail': 'Post already liked'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'detail': 'Post liked'}, status=201)

    def delete(self, request, post_id):
        post = generics.get_object_or_404(Post, id=post_id)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(status=204)


class CommentCreateListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = generics.get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(user=self.request.user, post=post)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True,context={'request': request})

        return Response(
            {
                "status": "success",
                "message": "Comments retrieved successfully",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

