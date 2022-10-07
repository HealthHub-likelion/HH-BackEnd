# Generated by Django 4.0.4 on 2022-10-06 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_merge_20221006_2010'),
        ('record', '0004_record_like_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('member_nickname', models.CharField(default='', max_length=150)),
                ('comment', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='댓글 작성 시간')),
                ('member_id', models.ForeignKey(db_column='member_id', on_delete=django.db.models.deletion.CASCADE, related_name='comment_member', to='accounts.member')),
                ('record_id', models.ForeignKey(db_column='record_id', on_delete=django.db.models.deletion.CASCADE, related_name='record_comments', to='record.record')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('member_nickname', models.CharField(default='', max_length=150)),
                ('comment', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='댓글 작성 시간')),
                ('comment_id', models.ForeignKey(db_column='comment_id', on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment_comment', to='record.comments')),
                ('member_id', models.ForeignKey(db_column='member_id', on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment_member', to='accounts.member')),
            ],
        ),
    ]
