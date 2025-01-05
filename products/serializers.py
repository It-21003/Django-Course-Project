from rest_framework import serializers
from .models import Product
from django.contrib.auth.hashers import make_password

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", 'name', 'description', 'price', 'stock', 'supplier', 'created_at', 'updated_at']
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        
        token['isAdmin'] = user.is_staff
        

        return token
    