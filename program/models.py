from django.db import models
from user.models import User


class ProgramsList(models.Model):
    id = models.AutoField("ID", db_column="ID", primary_key=True)
    onum = models.CharField("ONumber", max_length=255, db_column="ONumber")
    model_num = models.CharField(
        "ModelNum",
        max_length=255,
        db_column="ModelNum",
        null=True)
    parts_name = models.CharField(
        "PartsName",
        max_length=255,
        db_column="PartsName",
        null=True)
    goods_name = models.CharField(
        "GoodsName",
        max_length=255,
        db_column="GoodsName",
        null=True)
    files_name = models.CharField(
        "FilesName",
        max_length=255,
        db_column="FilesName",
        null=True)
    item_code = models.CharField(
        "ItemCode",
        max_length=255,
        db_column="ItemCode",
        null=True)
    tools = models.IntegerField("FilesName", db_column="Tools", null=True)
    creator = models.CharField(
        "Creator",
        max_length=255,
        db_column="Creator",
        null=True)
    tooling = models.CharField(
        "Tooling",
        max_length=255,
        db_column="Tooling",
        null=True)
    folder_path = models.CharField(
        "FolderPath",
        max_length=255,
        db_column="FolderPath",
        null=True)
    create_date = models.CharField(
        "CreateDate",
        max_length=50,
        db_column="CreateDate",
        null=True)
    process_time = models.CharField(
        "ProcessTime",
        max_length=50,
        db_column="ProcessTime",
        null=True)
    size = models.CharField(
        "Size",
        max_length=255,
        db_column="Size",
        null=True)
    comment1 = models.CharField(
        "Comment1",
        max_length=255,
        db_column="Comment1",
        null=True)
    comment2 = models.CharField(
        "Comment2",
        max_length=255,
        db_column="Comment2",
        null=True)

    class Meta:
        db_table = "Programs_list"


class ToolingsList(models.Model):
    id = models.AutoField("ID", db_column="ID", primary_key=True)
    program = models.ForeignKey(
        ProgramsList,
        related_name="toolings",
        verbose_name="Program",
        on_delete=models.CASCADE,
        db_column="ProgramID",
        to_field="id")
    onum = models.CharField("ONumber", max_length=255, db_column="ONumber")
    item_code = models.CharField(
        "ItemCode",
        max_length=255,
        db_column="ItemCode",
        null=True)
    files_name = models.CharField(
        "FilesName",
        max_length=255,
        db_column="FilesName",
        null=True)
    create_date = models.CharField(
        "CreateDate",
        max_length=50,
        db_column="CreateDate",
        null=True)
    tooling = models.CharField(
        "Tooling",
        max_length=255,
        db_column="Tooling",
        null=True)
    folder_path = models.CharField(
        "FolderPath",
        max_length=255,
        db_column="FolderPath",
        null=True)
    tnum = models.IntegerField("TNumber", db_column="TNumber", default=0)
    tool_name = models.CharField(
        "ToolName",
        max_length=255,
        db_column="ToolName",
        null=True)
    holder_name = models.CharField(
        "HolderName",
        max_length=255,
        db_column="HolderName",
        null=True)
    cut_distance = models.DecimalField(
        "CutDistance",
        max_digits=15,
        decimal_places=3,
        db_column="CutDistance",
        null=True)
    tip_name = models.CharField(
        "TipName",
        max_length=255,
        db_column="TipName",
        null=True)

    class Meta:
        db_table = "Toolings_list"


class NonePermanent(models.Model):
    id = models.AutoField("ID", db_column="ID", primary_key=True)
    tooling = models.CharField("Tooling", max_length=255, db_column="Tooling")
    tnum = models.IntegerField("TNumber", db_column="TNumber", default=0)

    class Meta:
        db_table = "Non_Permanent"


class ToolCheckHistory(models.Model):
    id = models.AutoField("ID", db_column="ID", primary_key=True)
    user = models.ForeignKey(
        User,
        related_name="tool_histories",
        verbose_name="User",
        on_delete=models.CASCADE,
        db_column="UserID",
        to_field="id")
    number = models.IntegerField("No", db_column="CheckNo", default=1)
    tooling = models.CharField(
        "Tooling",
        max_length=255,
        db_column="Tooling",
        null=True)
    program_info = models.CharField(
        "ONum String",
        max_length=255,
        db_column="ONum String",
        null=True)
    started_at = models.DateTimeField(
        'StartedAt', null=True, db_column="StartedAt")
    created_at = models.DateTimeField(
        'EndedAt', auto_now_add=True, db_column="EndedAt")

    class Meta:
        db_table = "Tool_Check_History"


class ToolCheckDetail(models.Model):
    id = models.AutoField("ID", db_column="ID", primary_key=True)
    history = models.ForeignKey(
        ToolCheckHistory,
        related_name="history_details",
        verbose_name="HistoryDetails",
        on_delete=models.CASCADE,
        db_column="HistoryID",
        to_field="id")
    tooling = models.CharField(
        "Tooling",
        max_length=255,
        db_column="Tooling",
        null=True,
        blank=True)
    tnum = models.IntegerField("TNumber", db_column="TNumber", default=0)
    tool_name = models.CharField(
        "ToolName",
        max_length=255,
        db_column="ToolName",
        null=True,
        blank=True)
    holder_name = models.CharField(
        "HolderName",
        max_length=255,
        db_column="HolderName",
        null=True,
        blank=True)
    tip_name = models.CharField(
        "TipName",
        max_length=255,
        db_column="TipName",
        null=True,
        blank=True)
    exchange = models.BooleanField(
        "Exchange", default=False, db_column="Exchange")
    correction = models.BooleanField(
        "Correction",
        default=False,
        db_column="Correction")

    class Meta:
        db_table = "Tool_Check_Detail"
