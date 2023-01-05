from rest_framework.test import APITestCase
from rest_framework.views import status

from django.shortcuts import resolve_url
from django.urls import reverse
from .models import *


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.reg_url = '/api/register'
        self.reg_login = '/api/login'
        self.regData = {
            "name": "user1",
            "email": "user1@gmail.com",
            "password": "qwer1234!"
        }

    def test_register(self):
        response = self.client.post(self.reg_url, data=self.regData, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
