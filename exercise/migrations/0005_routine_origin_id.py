# Generated by Django 4.0.6 on 2022-08-17 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0004_auto_20220816_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='origin_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]