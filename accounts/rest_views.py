from rest_framework import viewsets
from accounts.models import CustomUser, Profile
from accounts.serializers import CustomUserSerializer, ProfileSerializer, TopBuyerSerializer
from django.db.models import Sum
from django.db.models import F

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class TopBuyers(viewsets.ModelViewSet):
    serializer_class = TopBuyerSerializer

    def get_queryset(self):
        return Profile.objects.annotate(
        total_of_items=Sum(F('order__orderitem__quantity') * F('order__orderitem__product__price')),
        total_items_ordered=Sum('order__orderitem__quantity')
        ).order_by('total_items_ordered')

       