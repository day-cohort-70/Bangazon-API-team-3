"""View module for handling requests about customer shopping cart"""
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from bangazonapi.models import Order, Customer, Product, OrderProduct
from .product import ProductSerializer
from .order import OrderSerializer
from.lineitem import LineItemSerializer


class Cart(ViewSet):
    """Shopping cart for Bangazon eCommerce"""

    def create(self, request):
        """Add a product to the cart"""
        """
        @api {POST} /cart POST new line items to cart
        @apiName AddLineItem
        @apiGroup ShoppingCart

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        @apiParam {Number} product_id Id of product to add
        """
    

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /cart/:id DELETE line item from cart
        @apiName RemoveLineItem
        @apiGroup ShoppingCart

        @apiParam {id} id Product Id to remove from cart
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        current_user = Customer.objects.get(user=request.auth.user)
        open_order = Order.objects.get(
            customer=current_user, payment_type=None)

        line_item = OrderProduct.objects.filter(
            product__id=pk,
            order=open_order
        )[0]
        line_item.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """
        @api {GET} /cart GET line items in cart
        @apiName GetCart
        @apiGroup ShoppingCart

        @apiSuccess (200) {Number} id Order cart
        @apiSuccess (200) {String} url URL of order
        @apiSuccess (200) {String} created_date Date created
        @apiSuccess (200) {Object} payment_type Payment id use to complete order
        @apiSuccess (200) {String} customer URI for customer
        @apiSuccess (200) {Number} size Number of items in cart
        @apiSuccess (200) {Object[]} line_items Line items in cart
        @apiSuccess (200) {Number} line_items.id Line item id
        @apiSuccess (200) {Object} line_items.product Product in cart
        @apiSuccessExample {json} Success
            {
                "id": 2,
                "url": "http://localhost:8000/orders/2",
                "created_date": "2019-04-12",
                "payment_type": null,
                "customer": "http://localhost:8000/customers/7",
                "products": [
                    {
                        "id": 52,
                        "url": "http://localhost:8000/products/52",
                        "name": "900",
                        "price": 1296.98,
                        "number_sold": 0,
                        "description": "1987 Saab",
                        "quantity": 2,
                        "created_date": "2019-03-19",
                        "location": "Vratsa",
                        "image_path": null,
                        "average_rating": 0,
                        "category": {
                            "url": "http://localhost:8000/productcategories/2",
                            "name": "Auto"
                        }
                    }
                ],
                "size": 1
            }
        """

