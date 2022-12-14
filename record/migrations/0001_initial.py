# Generated by Django 4.0.4 on 2022-11-16 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exercise', '0001_initial'),
        ('accounts', '0001_initial'),
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
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='기록 작성 시간')),
                ('like_user', models.ManyToManyField(related_name='like_record', to='accounts.member')),
                ('member_id', models.ForeignKey(db_column='member_id', on_delete=django.db.models.deletion.CASCADE, related_name='record_member', to='accounts.member')),
                ('routine_id', models.ForeignKey(db_column='routine_id', on_delete=django.db.models.deletion.CASCADE, related_name='record_routine', to='exercise.routine')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='record_id',
            field=models.ForeignKey(db_column='record_id', on_delete=django.db.models.deletion.CASCADE, related_name='record_comments', to='record.record'),
        ),
    ]
