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

    def create(self, request):
        """Handle POST operations to like a product"""
        customer = Customer.objects.get(user=request.auth.user)
        product = Product.objects.get(pk=request.data["product_id"])

        like = Like.objects.create(customer=customer, product=product)
        like.save()
        serializer = LikeSerializer(like, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        """Handle GET requests to get all likes by the authenticated user"""

        likes = Like.objects.all()
        product = self.request.query_params.get("product", None)
        customer = self.request.query_params.get("customer", None)

        if product is not None:
            likes = likes.filter(product_id=product)

        if customer is not None:
            likes = likes.filter(customer_id=customer)

        serializer = LikeSerializer(likes, many=True, context={"request": request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to unlike a product"""
        try:
            like = Like.objects.get(pk=pk, customer__user=request.auth.user)
            like.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
