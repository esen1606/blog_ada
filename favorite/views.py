from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Favorite
from post.permissions import IsAuthor
from .serializers import FavoriteSerializer


# Create your views here.


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthor,)
    lookup_field = 'id'