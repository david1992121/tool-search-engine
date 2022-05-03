import json
import random
import string
from django.test import TestCase
from django.urls import reverse

from qrcode.models import Qrcode
from user.models import Token, User


class TestModel(TestCase):
    def setUp(self):
        self.qrcode = Qrcode.objects.create(aufnr="sample")

    def test_char_fields(self):
        fields = [{"field": "aufnr",
                   "verbose": "AUFNR",
                   "max_length": 12,
                   "is_null": False,
                   "value": "sample"},
                  {"field": "matnr",
                   "verbose": "MATNR",
                   "max_length": 18,
                   "is_null": True,
                   "value": None},
                  {"field": "dwerk",
                   "verbose": "DWERK",
                   "max_length": 4,
                   "is_null": True,
                   "value": None}]
        for field_item in fields:
            self.check_char_field(
                field_item["field"],
                field_item["verbose"],
                max_length=field_item["max_length"],
                value=field_item["value"],
                is_null=field_item["is_null"]
            )

    def check_char_field(
            self,
            field_name,
            verbose_name,
            max_length=255,
            is_null=True,
            value=None):
        meta_data = self.qrcode._meta.get_field(field_name)
        self.assertEqual(meta_data.verbose_name, verbose_name)
        self.assertEqual(meta_data.max_length, max_length)
        self.assertEqual(meta_data.null, is_null)
        self.assertEqual(getattr(self.qrcode, field_name), value)


class TestView(TestCase):
    databases = {'default', 'qr'}

    def setUp(self):
        self.databases = '__all__'
        self.qrcode = Qrcode.objects.using(
            'qr').create(aufnr="sample", matnr="00001")
        self.user = User.objects.create(name="test-user", id="00001")
        self.token = Token.objects.create(
            user=self.user,
            token=''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(32)
            ))

    def test_get_qrcode(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(
            reverse('item-code'), {"code": "sample"}, **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(res, "00001")
