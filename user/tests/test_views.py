


import json
import random
import string
from django.test import TestCase

from user.models import Token, User
from django.urls import reverse

class TestView(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="test-user", id="00001")
        self.token = Token.objects.create(
            user=self.user,
            token=''.join(
                    random.choice(
                        string.ascii_letters + string.digits
                    ) for _ in range(32)
            ))

    def test_register(self):
        response = self.client.post(reverse('user-register'), {
            'id': "12345",
            'name': 'test-user-001'
        })
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('user-login'), {
            'user_id': '00001'
        })
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertNotEqual(res["token"], "")
        self.assertEqual(res["data"]["id"], "00001")

    def test_info(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('user-info'), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(res["id"], "00001")

    def test_user_list(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('user-list'), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertLessEqual(1, len(res))

    def test_profile_name(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.put(reverse('user-change-name'), {
            "name": "test-user-changed"
        }, content_type="application/json", **auth_header)
        self.assertEqual(response.status_code, 200)