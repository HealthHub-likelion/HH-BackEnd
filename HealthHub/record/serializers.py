from exercise.models import Routine
from accounts.models import Member
from accounts.serializers import MemberSerializer
from exercise.serializers import RoutineOnlySerializer
from .models import Record
from rest_framework import serializers

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Record
        fields= '__all__'

class RoutineForRecordSerializer(serializers.ModelSerializer):
    record_routine = RecordSerializer(many=True)
    class Meta:
        model=Routine
        fields= ('id','routineName','record_routine')

class MemberForRoutineSerializer(serializers.ModelSerializer):
    routine_member = RoutineForRecordSerializer(many=True)
    # record_member = RecordSerializer(many=True)
    class Meta:
        model=Member
        fields= ('id','nickname','img','routine_member')

