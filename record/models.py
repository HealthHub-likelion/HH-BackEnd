from django.db import models
from accounts.models import Member
# Create your models here.
class Record(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey("accounts.Member", related_name="record_member", on_delete=models.CASCADE, db_column="member_id")
    like_user = models.ManyToManyField(Member,related_name='like_record')
    routine_id = models.ForeignKey("exercise.Routine", related_name="record_routine", on_delete=models.CASCADE, db_column="routine_id")
    comment = models.TextField()
    img = models.ImageField(blank=True, upload_to="images/", null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='기록 작성 시간')


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    record_id = models.ForeignKey("record.Record", related_name="record_comments", on_delete=models.CASCADE, db_column="record_id")
    member_id = models.ForeignKey("accounts.Member", related_name="comment_member", on_delete=models.CASCADE, db_column="member_id")
    member_nickname = models.CharField(default='', max_length=150, null=False)
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='댓글 작성 시간')
    
class ReplyComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey("record.Comments", related_name="reply_comment_comment", on_delete=models.CASCADE, db_column="comment_id")
    member_id = models.ForeignKey("accounts.Member", related_name="reply_comment_member", on_delete=models.CASCADE, db_column="member_id")
    member_nickname = models.CharField(default='', max_length=150, null=False)
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='댓글 작성 시간')