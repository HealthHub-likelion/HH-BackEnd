# Generated by Django 4.0.4 on 2022-08-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_member_isopen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='token',
            field=models.CharField(max_length=255),
        ),
    ]