from rest_framework import serializers
from .models import Post, PostImages
from category.models import Category
from like.serializers import LikeSerializer
from comment.serializers import CommentSerializer
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'



class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    first_name = serializers.ReadOnlyField(source='owner.first_name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category_name', 'previews', 'owner_username', 'first_name',)

        

class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    category =  serializers.PrimaryKeyRelatedField(
        required=True, queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ('title', 'body', 'previews', 'images', 'category')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(images=image, post=post)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    images = PostImageSerializer(many=True)
    first_name = serializers.ReadOnlyField(source = 'owher.first_name')
    category_name = serializers.ReadOnlyField(source = 'category.name')

    class Meta:
        model = Post
        fields = '__all__'

    
    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()
    
    @staticmethod
    def is_favorite(post, user):
        return user.favorites.filter(post=post).exists()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['quantity_of_likes'] = 0
        for _ in representation['likes']:
            representation['quantity_of_likes'] += 1
        user = self.context['request'].user
        representation['comment'] = CommentSerializer(instance.comments.all(), many = True).data
        representation['comments_count'] = instance.comments.count()
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance, user)
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation
    


