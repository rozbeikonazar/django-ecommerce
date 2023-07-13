from rest_framework import serializers

from accounts.models import CustomUser, Profile

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_login']

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    
    class Meta:
        model = Profile
        fields = ['profile_image', 'user']
    
class TopBuyerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    total_of_items = serializers.ReadOnlyField()
    total_items_ordered = serializers.ReadOnlyField()
    class Meta:
        model = Profile
        fields = ['user', 'total_of_items', 'total_items_ordered']

