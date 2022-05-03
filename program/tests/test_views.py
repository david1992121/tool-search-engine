

import json
import random
import string
from django.test import TestCase
from django.urls import reverse
from program.models import ProgramsList, ToolCheckDetail, ToolCheckHistory, ToolingsList
from user.models import Token, User


class TestProgramsAndTools(TestCase):
    def setUp(self):
        self.create_user()
        self.program = ProgramsList.objects.create(
            onum="onum",
            model_num="model-num",
            tools=5
        )
        self.tooling = ToolingsList.objects.create(
            program=self.program, onum="tooling-onum")               
        
    def create_user(self):
        self.user = User.objects.create(name="test-user", id="00001")
        self.token = Token.objects.create(
            user=self.user,
            token=''.join(
                    random.choice(
                        string.ascii_letters + string.digits
                    ) for _ in range(32)
            ))

    def test_get_programs(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('programs-list'), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertLessEqual(1, len(res))

    def test_get_toolings(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('toolings-list'), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertLessEqual(1, len(res))

    def test_get_tools(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(
            reverse('tools-list'), {"program_ids": "[{}]".format(self.program.id)}, **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertLessEqual(1, len(res))

    def test_download_pdf(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(
            reverse('download-pdf'), {"id": self.program.id, "type": ""}, **auth_header)
        self.assertEqual(response.status_code, 404)


class TestCheckHistoryDetail(TestCase):
    def setUp(self):
        self.create_user()
        self.history = ToolCheckHistory.objects.create(user=self.user)
        self.detail = ToolCheckDetail.objects.create(history=self.history)               
        
    def create_user(self):
        self.user = User.objects.create(name="test-user", id="00001")
        self.token = Token.objects.create(
            user=self.user,
            token=''.join(
                    random.choice(
                        string.ascii_letters + string.digits
                    ) for _ in range(32)
            ))

    def test_save_check_history(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.post(reverse('save-check-history'), {
            "number": 1,
            "tooling": "tooling",
            "onum": "onum",
            "started_at": "2022-04-01T10:00:00Z"
        }, **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(res["number"], 1)

    def test_save_check_detail(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.post(reverse('save-check-detail'), {
            "history_id": self.history.id,
            "tooling": "tooling",
        }, **auth_header)
        self.assertEqual(response.status_code, 200)

    def test_get_check_histories(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('history-list'), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(len(res), 1)

    def test_get_check_history(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('history-retrieve', kwargs={ 'id': self.history.id }), **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertEqual(res["id"], self.history.id)

    def test_get_check_detail_list(self):
        auth_header = {'HTTP_AUTHORIZATION': '{}'.format(self.token.token)}
        response = self.client.get(reverse('history-detail-list'), { 'detail_id': self.history.id }, **auth_header)
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.content)
        self.assertLessEqual(1, len(res))