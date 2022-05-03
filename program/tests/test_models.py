from django.test import TestCase

from program.models import NonePermanent, ProgramsList, ToolCheckDetail, ToolCheckHistory, ToolingsList
from user.models import User


class TestProgramsList(TestCase):
    def setUp(self):
        self.program = ProgramsList.objects.create(
            onum="onum",
            model_num="model-num",
            tools=5
        )

    def test_onum(self):
        meta_data = self.program._meta.get_field("onum")
        self.assertEqual(meta_data.verbose_name, "ONumber")
        self.assertEqual(meta_data.db_column, "ONumber")
        self.assertEqual(meta_data.max_length, 255)
        self.assertEqual(meta_data.null, False)
        self.program.onum = "onum"

    def test_tools(self):
        meta_data = self.program._meta.get_field("tools")
        self.assertEqual(meta_data.verbose_name, "FilesName")
        self.assertEqual(meta_data.db_column, "Tools")
        self.assertEqual(meta_data.null, True)
        self.program.tools = 5

    def test_char_fields(self):
        fields = [
            {"field": "model_num", "verbose": "ModelNum", "is_null": True, "max_length": 255, "value": "model-num"},
            {"field": "parts_name", "verbose": "PartsName", "is_null": True, "max_length": 255, "value": None},
            {"field": "goods_name", "verbose": "GoodsName", "is_null": True, "max_length": 255, "value": None},
            {"field": "files_name", "verbose": "FilesName", "is_null": True, "max_length": 255, "value": None},
            {"field": "item_code", "verbose": "ItemCode", "is_null": True, "max_length": 255, "value": None},
            {"field": "creator", "verbose": "Creator", "is_null": True, "max_length": 255, "value": None},
            {"field": "tooling", "verbose": "Tooling", "is_null": True, "max_length": 255, "value": None},
            {"field": "folder_path", "verbose": "FolderPath", "is_null": True, "max_length": 255, "value": None},
            {"field": "create_date", "verbose": "CreateDate", "is_null": True, "max_length": 50, "value": None},
            {"field": "process_time", "verbose": "ProcessTime", "is_null": True, "max_length": 50, "value": None},
            {"field": "size", "verbose": "Size", "is_null": True, "max_length": 255, "value": None},
            {"field": "comment1", "verbose": "Comment1", "is_null": True, "max_length": 255, "value": None},
            {"field": "comment2", "verbose": "Comment2", "is_null": True, "max_length": 255, "value": None}
        ]
        for field_item in fields:
            self.check_char_field(
                field_item["field"],
                field_item["verbose"],
                is_null=field_item["is_null"],
                max_length=field_item["max_length"],
                value=field_item["value"]
            )

    def check_char_field(
            self,
            field_name,
            verbose_name,
            max_length=255,
            is_null=True,
            value=None):
        meta_data = self.program._meta.get_field(field_name)
        self.assertEqual(meta_data.verbose_name, verbose_name)
        self.assertEqual(meta_data.max_length, max_length)
        self.assertEqual(meta_data.null, is_null)
        self.assertEqual(getattr(self.program, field_name), value)


class TestToolingsList(TestCase):
    def setUp(self):
        self.program = ProgramsList.objects.create(onum="onum")
        self.tooling = ToolingsList.objects.create(
            program=self.program, onum="tooling-onum")

    def test_program(self):
        self.assertEqual(self.tooling.program.id, self.program.id)

    def test_onum(self):
        meta_data = self.tooling._meta.get_field("onum")
        self.assertEqual(meta_data.verbose_name, "ONumber")
        self.assertEqual(meta_data.db_column, "ONumber")
        self.assertEqual(meta_data.max_length, 255)
        self.assertEqual(meta_data.null, False)
        self.tooling.onum = "tooling-onum"

    def test_tools(self):
        meta_data = self.tooling._meta.get_field("tnum")
        self.assertEqual(meta_data.verbose_name, "TNumber")
        self.assertEqual(meta_data.db_column, "TNumber")
        self.assertEqual(meta_data.null, False)
        self.tooling.tools = 0

    def test_char_fields(self):
        fields = [
            {"field": "item_code", "verbose": "ItemCode", "max_length": 255},
            {"field": "files_name", "verbose": "FilesName", "max_length": 255},
            {"field": "create_date", "verbose": "CreateDate", "max_length": 50},
            {"field": "tooling", "verbose": "Tooling", "max_length": 255},
            {"field": "folder_path", "verbose": "FolderPath", "max_length": 255},
            {"field": "tool_name", "verbose": "ToolName", "max_length": 255},
            {"field": "holder_name", "verbose": "HolderName", "max_length": 255},
            {"field": "tip_name", "verbose": "TipName", "max_length": 255}
        ]

        for field_item in fields:
            self.check_char_field(
                field_item["field"],
                field_item["verbose"],
                max_length=field_item["max_length"],
            )

    def check_char_field(
            self,
            field_name,
            verbose_name,
            max_length=255,
            is_null=True,
            value=None):
        meta_data = self.tooling._meta.get_field(field_name)
        self.assertEqual(meta_data.verbose_name, verbose_name)
        self.assertEqual(meta_data.max_length, max_length)
        self.assertEqual(meta_data.null, is_null)
        self.assertEqual(getattr(self.tooling, field_name), value)

    def check_cut_distance(self):
        meta_data = self.tooling._meta.get_field("cut_distance")
        self.assertEqual(meta_data.verbose_name, "CutDistance")
        self.assertEqual(meta_data.null, True)
        self.assertEqual(meta_data.max_digits, 15)
        self.assertEqual(meta_data.decimal_places, 3)
        self.assertEqual(self.tooling.cut_distance, None)


class TestNonPermanent(TestCase):
    def setUp(self):
        self.object = NonePermanent.objects.create(tooling="tooling")

    def test_tooling(self):
        meta_data = self.object._meta.get_field("tooling")
        self.assertEqual(meta_data.verbose_name, "Tooling")
        self.assertEqual(meta_data.db_column, "Tooling")
        self.assertEqual(meta_data.max_length, 255)
        self.assertEqual(meta_data.null, False)
        self.object.onum = "tooling"

    def test_tnum(self):
        meta_data = self.object._meta.get_field("tnum")
        self.assertEqual(meta_data.verbose_name, "TNumber")
        self.assertEqual(meta_data.db_column, "TNumber")
        self.assertEqual(meta_data.null, False)
        self.object.tools = 0


class TestToolCheckHistory(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="test-user")
        self.history = ToolCheckHistory.objects.create(user=self.user)

    def test_user(self):
        self.assertEqual(self.history.user.id, self.user.id)

    def test_number(self):
        meta_data = self.history._meta.get_field("number")
        self.assertEqual(meta_data.verbose_name, "No")
        self.assertEqual(meta_data.db_column, "CheckNo")
        self.assertEqual(meta_data.default, 1)
        self.history.number = 1

    def test_char_fields(self):
        fields = [
            {"field": "tooling", "verbose": "Tooling"},
            {"field": "program_info", "verbose": "ONum String"}
        ]
        for field_item in fields:
            self.check_char_field(
                field_item["field"],
                field_item["verbose"]
            )

    def check_char_field(
            self,
            field_name,
            verbose_name,
            max_length=255,
            is_null=True,
            value=None):
        meta_data = self.history._meta.get_field(field_name)
        self.assertEqual(meta_data.verbose_name, verbose_name)
        self.assertEqual(meta_data.max_length, max_length)
        self.assertEqual(meta_data.null, is_null)
        self.assertEqual(getattr(self.history, field_name), value)

    def test_created_at(self):
        meta_data = self.history._meta.get_field('created_at')
        self.assertEqual(meta_data.verbose_name, 'EndedAt')
        self.assertEqual(meta_data.auto_now_add, True)
        self.assertEqual(meta_data.auto_now, False)


class TestToolCheckDetail(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="test-user")
        self.history = ToolCheckHistory.objects.create(user=self.user)
        self.detail = ToolCheckDetail.objects.create(history=self.history)

    def test_history(self):
        self.assertEqual(self.detail.history.id, self.history.id)

    def test_tnum(self):
        meta_data = self.detail._meta.get_field("tnum")
        self.assertEqual(meta_data.verbose_name, "TNumber")
        self.assertEqual(meta_data.db_column, "TNumber")
        self.assertEqual(meta_data.null, False)
        self.detail.tools = 0

    def test_exchange(self):
        meta_data = self.detail._meta.get_field("exchange")
        self.assertEqual(meta_data.verbose_name, "Exchange")
        self.assertEqual(meta_data.db_column, "Exchange")
        self.assertEqual(meta_data.null, False)
        self.detail.exchange = False

    def test_correction(self):
        meta_data = self.detail._meta.get_field("correction")
        self.assertEqual(meta_data.verbose_name, "Correction")
        self.assertEqual(meta_data.db_column, "Correction")
        self.assertEqual(meta_data.null, False)
        self.detail.correction = False

    def test_char_fields(self):
        fields = [
            {"field": "tooling", "verbose": "Tooling"},
            {"field": "tool_name", "verbose": "ToolName"},
            {"field": "holder_name", "verbose": "HolderName"},
            {"field": "tip_name", "verbose": "TipName"}
        ]
        for field_item in fields:
            self.check_char_field(
                field_item["field"],
                field_item["verbose"]
            )

    def check_char_field(
            self,
            field_name,
            verbose_name,
            max_length=255,
            is_null=True,
            value=None):
        meta_data = self.detail._meta.get_field(field_name)
        self.assertEqual(meta_data.verbose_name, verbose_name)
        self.assertEqual(meta_data.max_length, max_length)
        self.assertEqual(meta_data.null, is_null)
        self.assertEqual(getattr(self.detail, field_name), value)
