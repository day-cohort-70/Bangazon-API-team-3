
"""View module for handling requests about line items"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import OrderProduct, Order, Product, Customer


class LineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for line items """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='lineitem',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product')

class LineItems(ViewSet):
    """Line items for Bangazon orders"""

    # TIP: By setting this class attribute, then a `basename` parameter
    #      does not need to be set on the route in urls.py:11 and allow
    #      the serializer (see above) use the `view_name='lineitem'`
    #      argument for the HyperlinkedIdentityField. If this is NOT set
    #      then the following exception gets thrown.
    #
    # ImproperlyConfigured at /lineitems/4
    #   Could not resolve URL for hyperlinked relationship using view name
    #   "orderproduct-detail". You may have failed to include the related
    #   model in your API, or incorrectly configured the `lookup_field`
    #   attribute on this field.
    # queryset = OrderProduct.objects.all()


    def update(self, request, pk=None):
        """Update the quantity of a product in the cart"""
        try:
            # Get the current user
            current_user = Customer.objects.get(user=request.auth.user)

            # Get the open order (cart) for the current user
            open_order = Order.objects.get(customer=current_user, payment_type=None)

            # Get the line item
            line_item = OrderProduct.objects.get(pk=pk, order=open_order)

            # Get the new quantity from the request data
            new_quantity = request.data.get('quantity')

            # Ensure the new quantity is a positive integer
            if new_quantity is not None and isinstance(new_quantity, int) and new_quantity > 0:
                line_item.quantity = new_quantity
                line_item.save()
                return Response({
                    'message': 'Quantity updated',
                    'product': line_item.product.name,
                    'quantity': line_item.quantity
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Invalid quantity. Please provide a positive integer.'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response({
                'message': 'Customer not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({
                'message': 'No open order found'
            }, status=status.HTTP_404_NOT_FOUND)
        except OrderProduct.DoesNotExist:
            return Response({
                'message': 'Product not found in cart'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                'message': str(ex)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """
        @api {GET} /cart/:id DELETE line item from cart
        @apiName RemoveLineItem
        @apiGroup ShoppingCart

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} id Product Id to remove from cart
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            # line_item = OrderProduct.objects.get(pk=pk)
            customer = Customer.objects.get(user=request.auth.user)
            line_item = OrderProduct.objects.get(pk=pk, order__customer=customer)

            serializer = LineItemSerializer(line_item, context={'request': request})

            return Response(serializer.data)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /cart/:id DELETE line item from cart
        @apiName RemoveLineItem
        @apiGroup ShoppingCart

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} id Product Id to remove from cart
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            customer = Customer.objects.get(user=request.auth.user)
            order_product = OrderProduct.objects.get(pk=pk, order__customer=customer)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
