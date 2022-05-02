from django.db import models

# Create your models here.


class Qrcode(models.Model):
    aufnr = models.CharField(
        "AUFNR",
        max_length=12,
        primary_key=True,
        db_column="AUFNR")
    matnr = models.CharField(
        "MATNR",
        max_length=18,
        null=True,
        db_column="MATNR")
    dwerk = models.CharField(
        "DWERK",
        max_length=4,
        null=True,
        db_column="DWERK")

    class Meta:
        db_table = "SAP_PPT_FL_AFPO"
