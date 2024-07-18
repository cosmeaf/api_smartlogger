from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    repeat_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'repeat_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if len(attrs['password']) < 6:
            raise serializers.ValidationError({"password": "Password must be at least 6 characters long."})

        if not any(char.isdigit() for char in attrs['password']):
            raise serializers.ValidationError({"password": "Password must contain at least one digit."})

        if not any(char.isalpha() for char in attrs['password']):
            raise serializers.ValidationError({"password": "Password must contain at least one letter."})

        if not any(char in '!@#$%^&*()' for char in attrs['password']):
            raise serializers.ValidationError({"password": "Password must contain at least one special character."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Validar o comprimento do nome de usuário e senha
        if len(attrs.get('username', '')) < 6:
            raise serializers.ValidationError({'username': 'Username must be at least 6 characters long.'})
        if len(attrs.get('password', '')) < 6:
            raise serializers.ValidationError({'password': 'Password must be at least 6 characters long.'})
        
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
        }
        return data


