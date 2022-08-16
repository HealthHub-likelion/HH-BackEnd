from itertools import count
from django.db import models
from numpy import integer

# Create your models here.
class Routine(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey("accounts.Member", related_name="routine_member", on_delete=models.CASCADE, db_column="member_id",null=True,blank=True)
    creator_id = models.ForeignKey("accounts.Member", related_name="routine_creator", on_delete=models.CASCADE, db_column="creator_id",null=True,blank=True)
    routineName = models.CharField(max_length=20)
    isOpen = models.BooleanField()
    count = models.IntegerField(default=0)


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    en_name = models.CharField(max_length=50)
    ko_name = models.CharField(max_length=40,unique=True)
    part = models.CharField(max_length=40)


class RoutineExercise(models.Model):
    id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey("Routine", related_name="re_routine", on_delete=models.CASCADE, db_column="routine_id")
    exercise_id= models.ForeignKey("Exercise" ,related_name="re_exercise", on_delete=models.CASCADE, db_column="exercise_id",null=True)


class Set(models.Model):
    id = models.AutoField(primary_key=True)
    routine_exercise_id= models.ForeignKey("RoutineExercise", related_name="set_exercise", on_delete=models.CASCADE, db_column="routine_exercise_id",null=True)
    count = models.IntegerField()
    weight = models.IntegerField()