from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    password_confirmation = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')

    def validate(self, attrs):
        password_confirmation = attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError(
                'The name bust begin with a capital letter'
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        request = self.context.get('request')
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        if username and password:
            user = authenticate(username=username,
                                password=password,
                                request=request,)
            if not user:
                raise serializers.ValidationError(
                    'Invalid username or password'
                )
        else:
            raise serializers.ValidationError(
                'Username and password must be fielded in'
            )
        data['user'] = user
        return data

    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Username is not found'
            )
        return username
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'last_name', 'first_name', 'email')
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
    
