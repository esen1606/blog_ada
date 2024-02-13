from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer
from .permissions import IsAuthorOrAdmin, IsAuthor
from rest_framework import generics
from rest_framework.filters import SearchFilter
from like.models import Like
from like.serializers import LikeSerializer
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer
from comment.serializers import CommentActionSerializer, CommentSerializer
from rest_framework.pagination import  PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class StandartPaginational(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data
        })
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartPaginational
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'category__id')
    filterset_fields = ('title', 'category')

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return PostCreateSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthorOrAdmin()]
        return [IsAuthenticated()]
    
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == "POST":
            if user.likes.filter(post=post).exists():
                return Response('This post has arleady liked', status=201)
            Like.objects.create(owner=user, post=post)
        elif request.method == "DELETE":
            likes = user.likes.filter(post=post)
            if likes.exists():
                likes.delete()
                return Response('Like is deleted', status=204)
            return Response('Post not found', status=404)
        else:
            likes = post.likes.all()
            serializer = LikeSerializer(instance=likes, many=True)
            return Response(serializer.data, status=200)
        
    @action(['POST', 'DELETE', 'GET'], detail=True)
    def favorite(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(post=post).exists():
                return Response('This post already in favorite', status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response('Added to the Favorites', status=201)
        elif request.method == 'DELETE':
            favorite = user.favorites.filter(post=post)
            if favorite.exists():
                favorite.delete()
                return Response('You deleted post is favorite', status=204)
            return Response('Post is no founded', status=404)
        else:
            favorites = user.favorites.all()
            if favorites.exists():
                serializer = FavoriteSerializer(instance=favorites, many=True)
                return Response(serializer.data, status=200)
            
    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comment(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            serializer = CommentActionSerializer(data=request.data,context={'post':post.id,'owner':user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)
        elif request.method == 'DELETE':
            comment_id = self.request.query_params['id']
            comment = post.comments.filter(post=post, pk=comment_id)    
            if comment.exists():
                comment.delete()
                return Response('The comment is delete', status=204)
            return Response('The comment not founded', status=404) 
        else: comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

class PostLIstCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostListSerializer
    
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Post.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == "DELETE":
            return (IsAuthorOrAdmin(),)
        elif self.request.method in ["PUT", "PATCH"]:
            return (IsAuthor(),)
        return (AllowAny(),)
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PostCreateSerializer
        return PostDetailSerializer
