from django_resized import ResizedImageField
from django.db import models

def user_directory_path(instance, filename):
    return 'static/avatar/{0}/{1}'.format(instance.id, filename)
class User(models.Model):
    """ User Model """
    id = models.CharField("従業員番号", max_length=5, unique=True, primary_key=True, db_column="UserID")
    name = models.CharField('名前', max_length=100, null=True, db_column="UserName")
    avatar = ResizedImageField('アバター', size = [500, 500], crop = ['middle', 'center'], quality=75,
        null = True, upload_to = user_directory_path, db_column="Avatar")
    
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