from django import db
from django.db import models

class User(models.Model):
    """ User Model """
    id = models.CharField("従業員番号", max_length=5, unique=True, primary_key=True, db_column="UserID")
    name = models.CharField('名前', max_length=100, null=True, db_column="UserName")
    avatar = models.ImageField('アバター', null = True, upload_to = "static/avatar", db_column="Avatar")
    
    class Meta:
        db_table = "Users"

    def is_authenticated(self):
        return True

class Token(models.Model):
    """ Token Model """
    id = models.AutoField('ID', primary_key=True, db_column='ID')
    token = models.CharField('キー', max_length=50, db_column="Token")
    user = models.ForeignKey(User, related_name="tokens", on_delete=models.CASCADE, verbose_name="ユーザー", 
        db_column="UserID", to_field="id")
    created_at = models.DateTimeField('作成日時', auto_now_add=True, db_column="CreatedAt")