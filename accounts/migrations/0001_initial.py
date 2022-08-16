# Generated by Django 3.2.14 on 2022-08-07 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('readMe', models.TextField()),
                ('email', models.EmailField(default='', max_length=150, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('token', models.CharField(max_length=255)),
                ('isOpen', models.BooleanField(default=True)),
                ('img', models.ImageField(blank=True, default='default', null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('follower_id', models.ForeignKey(db_column='follower_id', on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='accounts.member')),
                ('following_id', models.ForeignKey(db_column='following_id', on_delete=django.db.models.deletion.CASCADE, related_name='following', to='accounts.member')),
            ],
        ),
    ]