from .models import Exercise,Routine,RoutineExercise,Set
from rest_framework import serializers

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exercise
        # fields= '__all__'
        fields = ('en_name','ko_name','part','id')


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Set
        fields= '__all__'



class RoutineExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoutineExercise
        # fields=  ('id','routine_id')
        fields= '__all__'


class RoutineSerializer(serializers.ModelSerializer):
    # re_connect_ex = RoutineExerciseSerializer(source='RoutineExercise')
    # re_connect_ex =  serializers.RelatedField(many=True)
    class Meta:
        model=Routine
        fields= '__all__'
        # fields= ('id','creatorName','routineName','count','isOpen','member_id','RE_list')
    
    # def get_RE_list(self,obj):
    #     routine_query = RoutineExercise.objects.filter(
    #         # re_routine = obj.id
    #         routine_id = obj.id
    #     )   
    #     serializer =  RoutineExerciseSerializer(routine_query,many=True)
    #     return serializer.data
