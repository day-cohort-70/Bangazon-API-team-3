from rest_framework import serializers
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from bangazonapi.models import Store, Product, Customer
from rest_framework.permissions import IsAuthenticated


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class StoreSerializer(serializers.ModelSerializer):
    seller = UserSerializer(source="seller.user", read_only=True)
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Store
        fields = ["id", "name", "description", "seller", "product_count"]


class Stores(ViewSet):

    def list(self, request):
        stores = Store.objects.annotate(product_count=Count("products"))
        serializer = StoreSerializer(stores, many=True, context={"request": request})
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StoreSerializer(data=request.data)
        seller = Customer.objects.get(user=request.auth.user)
        if serializer.is_valid():
            serializer.save(seller=seller)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
