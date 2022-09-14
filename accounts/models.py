from email.policy import default
from django.db import models

def user_directory_path(instance, filename):
        return 'images/{0}'.format(instance.nickname + "_" + filename)

# Create your models here.
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(unique=True,max_length=20)
    readMe = models.TextField()
    email = models.EmailField(default='', max_length=150, null=False, blank=False, unique=True)
    password = models.TextField()
    token =  models.CharField(max_length=255)
    isOpen = models.BooleanField(default=True)
    img = models.ImageField(default='default',blank=True, upload_to = '', null=True)

    def __str__(self):
        return str(self.nickname)

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    following_id = models.ForeignKey("Member", related_name="following", on_delete=models.CASCADE, db_column="following_id", null=False)
    follower_id = models.ForeignKey("Member", related_name="follower", on_delete=models.CASCADE, db_column="follower_id", null=False)