from django.test import TestCase

from user.models import Token, User


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="test-user", id="00001")

    def test_id(self):
        meta_data = self.user._meta.get_field("id")
        self.assertEqual(meta_data.verbose_name, "従業員番号")
        self.assertEqual(meta_data.db_column, "UserID")
        self.assertEqual(meta_data.unique, True)
        self.assertEqual(meta_data.primary_key, True)
        self.assertEqual(meta_data.null, False)
        self.assertEqual(self.user.id, "00001")

    def test_name(self):
        meta_data = self.user._meta.get_field("name")
        self.assertEqual(meta_data.verbose_name, "名前")
        self.assertEqual(meta_data.db_column, "UserName")
        self.assertEqual(meta_data.max_length, 100)
        self.assertEqual(meta_data.null, True)
        self.user.name = "test-user"

    def test_avatar(self):
        meta_data = self.user._meta.get_field("avatar")
        self.assertEqual(meta_data.verbose_name, "アバター")
        self.assertEqual(meta_data.db_column, "Avatar")
        self.assertEqual(meta_data.quality, 75)
        self.assertEqual(meta_data.null, True)
        self.user.avatar = None

    def test_is_authenticated(self):
        self.assertTrue(self.user.is_authenticated())


class TestToken(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="test-user")
        self.token = Token.objects.create(user=self.user, token="1234567890")

    def test_user(self):
        self.assertEqual(self.token.user.id, self.user.id)

    def test_token(self):
        meta_data = self.token._meta.get_field("token")
        self.assertEqual(meta_data.verbose_name, "キー")
        self.assertEqual(meta_data.db_column, "Token")
        self.assertEqual(meta_data.max_length, 50)
        self.assertEqual(self.token.token, "1234567890")

    def test_created_at(self):
        meta_data = self.token._meta.get_field('created_at')
        self.assertEqual(meta_data.verbose_name, '作成日時')
        self.assertEqual(meta_data.auto_now_add, True)
        self.assertEqual(meta_data.auto_now, False)
