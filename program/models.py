from django.db import models

# Create your models here.
class ProgramsList(models.Model):
    onum = models.CharField("ONumber", max_length=255, db_column="ONumber")
    model_num = models.CharField("ModelNum", max_length=255, db_column="ModelNum", null=True)
    parts_name = models.CharField("PartsName", max_length=255, db_column="PartsName", null=True)
    goods_name = models.CharField("GoodsName", max_length=255, db_column="GoodsName", null=True)
    files_name = models.CharField("FilesName", max_length=255, db_column="FilesName", null=True)
    item_code = models.CharField("ItemCode", max_length=255, db_column="ItemCode", null=True)
    tools = models.IntegerField("FilesName", db_column="Tools", null=True)
    creator = models.CharField("Creator", max_length=255, db_column="Creator", null=True)
    tooling = models.CharField("Tooling", max_length=255, db_column="Tooling", null=True)
    folder_path = models.CharField("FolderPath", max_length=255, db_column="FolderPath", null=True)
    create_date = models.CharField("CreateDate", max_length=50, db_column="CreateDate", null=True)
    process_time = models.CharField("ProcessTime", max_length=50, db_column="ProcessTime", null=True)

    class Meta:
        db_table = "Programs_list"

class ToolingsList(models.Model):
    onum = models.CharField("ONumber", max_length=255, db_column="ONumber")
    item_code = models.CharField("ItemCode", max_length=255, db_column="ItemCode", null=True)
    files_name = models.CharField("FilesName", max_length=255, db_column="FilesName", null=True)
    create_date = models.CharField("CreateDate", max_length=50, db_column="CreateDate", null=True)
    tooling = models.CharField("Tooling", max_length=255, db_column="Tooling", null=True)
    folder_path = models.CharField("FolderPath", max_length=255, db_column="FolderPath", null=True)
    tnum = models.CharField("TNumber", max_length=255, db_column="TNumber", null=True)
    tool_name = models.CharField("ToolName", max_length=255, db_column="ToolName", null=True)
    holder_name = models.CharField("HolderName", max_length=255, db_column="HolderName", null=True)
    cut_distance = models.DecimalField("CutDistance", max_digits=8, decimal_places=3, db_column="CutDistance", null=True)

    class Meta:
        db_table = "Toolings_list"