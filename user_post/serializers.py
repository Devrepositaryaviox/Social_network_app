from rest_framework import serializers
from user_post.models import Post
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['descriptions', 'image', 'created_at', 'updated_at', 'user', 'id', 'like', 'total_likes']

    def get_total_likes(self, instance):
        return instance.like.count()
    
class RegisterationUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
      write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email_ = serializers.EmailField(
        label="Email Address", 
        required=True,
        write_only=True,
      )
      
    class Meta:
        model = User
        fields = ('username', 'email_', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
          'first_name': {'required': True},
          'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
          raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
    
    def validate_email_(self,attrs):
        try:
            validate_email(attrs)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError("email field must be unique")
        return attrs
        
    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['email_'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name'],
          email=validated_data['email_']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def to_representation(self, instance):
        representations = super().to_representation(instance)
        representations.pop('first_name')
        representations.pop('last_name')
        return representations

                                                        