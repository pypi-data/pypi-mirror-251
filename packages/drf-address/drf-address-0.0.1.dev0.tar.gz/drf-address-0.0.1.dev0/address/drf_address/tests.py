import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Address, Country
from .serializers import AddressSerializer

client = APIClient()

class AddressTest(TestCase):
    # @classmethod
    def setUp(self):
        self.country = Country.objects.create(name="India", code="IN")
        self.address = Address.objects.create(
            apartment='B-20', street='BSZ Marg', district='New Delhi', city='New Delhi', 
            postal_code='110002', state='Delhi', country=self.country
        )
        
    def test_add_country(self):
        self.assertEqual(self.country.name, 'India')
        self.assertEqual(self.country.code, 'IN')
    
    def test_add_address(self):
        self.assertEqual(self.address.apartment, 'B-20')
        self.assertEqual(self.address.street, 'BSZ Marg')
        self.assertEqual(self.address.district, 'New Delhi')
        self.assertEqual(self.address.city, 'New Delhi')
        self.assertEqual(self.address.state, 'Delhi')
        self.assertEqual(self.address.country.code, 'IN')
        
    def test_api_read_address(self):
        res = client.get(reverse('address-detail', kwargs={'pk': self.address.id}))
        address = AddressSerializer(self.address)
        self.assertEqual(address.data['apartment'], res.data['apartment'])
        self.assertEqual(address.data['street'], res.data['street'])
        self.assertEqual(address.data['district'], res.data['district'])
        self.assertEqual(address.data['city'], res.data['city'])
        self.assertEqual(address.data['state'], res.data['state'])
        self.assertEqual(res.data['country'], address.data['country'])
        
    # def test_api_create_address(self):
    #     data = {
    #         "country": "IN",
    #         "apartment": "B-20",
    #         "street": "First Floor, Vikram Nagar, Feroz Shah Kotla",
    #         "district": "New Delhi",
    #         "city": "New Delhi",
    #         "postal_code": "110002",
    #         "state": "Delhi"
    #     }
    #     res = client.post(reverse('address-list'), data=data)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)