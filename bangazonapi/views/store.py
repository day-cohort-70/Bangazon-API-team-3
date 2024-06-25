from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from bangazonapi.models import Store, Product
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",  # Add this field
            "username",
            "email",
            "first_name",
            "last_name",
        ]  # Add other fields as needed


class StoreSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ["id", "name", "description", "seller", "product_count"]

    def get_product_count(self, obj):
        return Product.objects.filter(store=obj).count()


class Stores(ViewSet):

    def list(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True, context={"request": request})
        return Response(serializer.data)
