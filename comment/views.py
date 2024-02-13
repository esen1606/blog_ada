from django.shortcuts import render
from .models import Comment
from rest_framework import generics, permissions
from post.permissions import IsAuthor
from .serializers import CommentSerializer

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permissions = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthor(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]