from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'Username is required.',
            'blank': 'Username cannot be blank.'
        }
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        trim_whitespace=False,
        error_messages={
            'required': 'Password is required.',
            'blank': 'Password cannot be blank.'
        }
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError({
                'detail': 'User with this username does not exist.',
                'error': 'User with this username does not exist.'
            })

        if not user.check_password(password):
            raise serializers.ValidationError({
                'detail': 'Incorrect password.',
                'error': 'Incorrect password.'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'User account is inactive.',
                'error': 'User account is inactive.'
            })

        attrs['user'] = user
        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
