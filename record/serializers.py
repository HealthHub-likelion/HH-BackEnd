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

# class RoutineForRecordSerializer(serializers.ModelSerializer):
#     record_routine = RecordSerializer(many=True)
#     class Meta:
#         model=Routine
#         fields= ('id','routineName','record_routine','isOpen')

# class MemberForRoutineSerializer(serializers.ModelSerializer):
#     routine_member = RoutineForRecordSerializer(many=True)
#     # record_member = RecordSerializer(many=True)
#     class Meta:
#         model=Member
#         fields= ('id','nickname','img','routine_member','isOpen')

class MemberForRecordSerializer(serializers.ModelSerializer):
    record_member = RecordSerializer(many=True)
    class Meta:
        model=Member
        fields= ('id','nickname','img','record_member','isOpen')



#멤버 <- 루틴 <- 레코드
#멤버 <- 레코드, 루틴 아이디 이용해서 루틴 정보 받아오기. 