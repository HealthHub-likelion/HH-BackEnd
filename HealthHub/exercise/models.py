from itertools import count
from django.db import models

# Create your models here.
class Routine(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey("accounts.Member", related_name="routine_member", on_delete=models.CASCADE, db_column="member_id")
    creatorName = models.CharField(max_length=20)
    routineName = models.CharField(max_length=20)
    count = models.IntegerField(default=0)
    isOpen = models.BooleanField()


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    en_name = models.CharField(max_length=40)
    ko_name = models.CharField(max_length=40)
    part = models.CharField(max_length=40)

class RoutineExercise(models.Model):
    id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey("Routine", related_name="re_routine", on_delete=models.CASCADE, db_column="routine_id")
    exercise_id= models.ForeignKey("Exercise", related_name="re_exercise", on_delete=models.CASCADE, db_column="exercise_id")


class Set(models.Model):
    id = models.AutoField(primary_key=True)
    exercise_id= models.ForeignKey("Exercise", related_name="set_exercise", on_delete=models.CASCADE, db_column="exercise_id")
    set_count = models.IntegerField()
    weight = models.IntegerField()

