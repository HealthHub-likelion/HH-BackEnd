from .models import Exercise,Routine,RoutineExercise,Set
from rest_framework import serializers

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exercise
        # fields= '__all__'
        fields = ('en_name','ko_name','part')


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Set
        fields= '__all__'



class RoutineExerciseSerializer(serializers.ModelSerializer):
    set_exercise = SetSerializer(many=True)
    class Meta:
        model=RoutineExercise
        # fields=  ('id','routine_id')
        fields= '__all__'

class RoutineExerciseOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model=RoutineExercise
        fields= '__all__'


class RoutineSerializer(serializers.ModelSerializer):
    re_routine = RoutineExerciseSerializer(many=True)
    class Meta:
        model=Routine
        fields= ('id')
        fields= ('id','creatorName','routineName','isOpen','member_id','count','re_routine')
    
class RoutineOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model=Routine
        fields= '__all__'
