from django.http import HttpResponseServerError
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from bangazonapi.models import Like, Product, Customer


class LikeSerializer(serializers.ModelSerializer):
    """JSON serializer for likes"""

    class Meta:
        model = Like
        fields = ("id", "customer", "product", "created_date")


class Likes(viewsets.ModelViewSet):
    """Handles likes for products"""

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def list(self, request):
        """Handle GET requests to get all likes by the authenticated user"""

        product = self.request.query_params.get("product", None)
        customer = self.request.query_params.get("customer", None)

        if product is None and customer is None:
            return Response(
                {"message": "Please provide a product or customer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        likes = Like.objects.all()

        if product is not None:
            likes = likes.filter(product_id=product)

        if customer is not None:
            likes = likes.filter(customer_id=customer)

        serializer = LikeSerializer(likes, many=True, context={"request": request})

        return Response(serializer.data)
