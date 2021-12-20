from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
from rest_framework import status
from .models import Customer, Provider, ProductProvider, Product

# Create your tests here.


class CustomerTest(TestCase):

    def setUp(self):
        self.client_stub = Client()
        self.credentials = {
            'username': 'cuicab',
            'email': 'cuicab95@gmail.com',
            'password': 'carlos'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client.login(username="cuicab", password="carlos")
        self.customer = {
            'first_name': 'Carlos',
            'last_name': 'Uicab',
            'code': '3332',
            'type': 'ORO'
        }
        self.customer = Customer.objects.create(**self.customer)
        self.provider = {
            'name': 'LG',
            'address': 'Callejón 34'
        }
        self.provider = Provider.objects.create(**self.provider)
        self.product = {
            'name': 'LG',
            'code': '6665',
            'description': 'Pantalla 45 pulgadas'
        }
        self.product = Product.objects.create(**self.product)
        self.product_provider = {
            'product_id': self.product.id,
            'provider_id': self.provider.id,
            'price': 34303
        }
        self.product_provider = ProductProvider.objects.create(**self.product_provider)
        self.valid_order = {
            "customer_id": self.customer.id,
            "is_urgent": True,
            "type": "CD",
            "items": [{"product_id": self.product.id, "quantity": 2}],
            "additional_data": {"stock": "Almacen 1"}
        }
        self.invalid_order = {
            "customer_id": self.customer.id,
            "is_urgent": True,
            "type": "CD",
            "items": [],
            "additional_data": {}
        }

    def test_order_route(self):
        response = self.client_stub.get(reverse('store:api:create-order'))
        self.assertEquals(response.status_code, 200)

    def test_valid_new_order_route(self):
        response = self.client.post(
            reverse('store:api:create-order'),
            data=json.dumps(self.valid_order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_new_order_route(self):
        response = self.client.post(
            reverse('store:api:create-order'),
            data=json.dumps(self.invalid_order),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


