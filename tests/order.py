import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase


class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user_id = json_response['id']

        # Create a store
        url = "/stores"
        store_data = {"name": "Big Bucks", "description": "a store"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        store_response = self.client.post(url, store_data, format='json')
        self.assertEqual(store_response.status_code, status.HTTP_201_CREATED)
        store_json = json.loads(store_response.content)
        self.store_id = store_json['id']
        print(f"Store ID: {self.store_id}")

        # Create a product category
        url = "/productcategories"
        category_data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        category_response = self.client.post(url, category_data, format='json')
        self.assertEqual(category_response.status_code, status.HTTP_201_CREATED)
        category_json = json.loads(category_response.content)
        self.category_id = category_json['id']

        # Create a product
        url = "/products"
        product_data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": self.category_id, "location": "Pittsburgh", "store_id": self.store_id }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        product_response = self.client.post(url, product_data, format='json')
        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)


    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    def test_complete_order_with_payment(self):
        """
        Ensure that an order can be completed with a PUT request containing the payment ID
        """
        #add item to cart
        self.test_add_product_to_order()

        #create a payment type
        url = "/paymenttypes"
        data = {
        "merchant_name": "American Express",
        "account_number": "111-1111-1111",
        "expiration_date": "2024-12-31",
        "create_date": datetime.date.today().isoformat()
    }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment_id = response.json()['id']

        #add payment
        url = "/orders/1"
        data = { "payment_type": payment_id }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        #fetch the order again to verify changes were made
        response = self.client.get(f"/orders/1")
        json_response = json.loads(response.content)

        #assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["payment_type"], payment_id)
    # TODO: New line item is not added to closed order