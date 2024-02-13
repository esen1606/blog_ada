from rest_framework import serializers
from .models import Favorite



class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['post_title'] = instance.post.title
        if instance.post.previews:
            preview = instance.post.previews
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation