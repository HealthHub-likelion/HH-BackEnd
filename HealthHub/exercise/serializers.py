from .models import Exercise,Routine,RoutineExercise,Set
from rest_framework import serializers

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exercise
        fields= '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Routine
        fields= '__all__'
        # fields= ("creatorName","routineName","count","isOpen")


class RoutineExerciseSerializer(serializers.ModelSerializer):
    # routines = RoutineSerializer()
    # exercise = ExerciseSerializer()
    class Meta:
        model=RoutineExercise
        # fields= ("routines","exercises")
        fields= '__all__'
    


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Set
        fields= '__all__'