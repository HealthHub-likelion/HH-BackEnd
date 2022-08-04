# Generated by Django 4.0.6 on 2022-08-03 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='exercise_id',
        ),
        migrations.AddField(
            model_name='set',
            name='routine_exercise_id',
            field=models.ForeignKey(db_column='routine_exercise_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set_exercise', to='exercise.routineexercise'),
        ),
    ]