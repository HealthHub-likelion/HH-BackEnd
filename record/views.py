from urllib import response
from django.shortcuts import render,get_object_or_404
from itsdangerous import Serializer

from exercise.models import Routine, RoutineExercise, Set
from .models import Record
from accounts.models import Member,Follow
from .serializers import RecordSerializer,MemberForRoutineSerializer,MemberForRecordSerializer
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q

class ymRecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()

    def create(self,request):
        #기록 생성
        data=request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        record_id = data["id"]

        #루틴 count 올려주기
        # data = json.loads(data)
        # print(data)
        routine_id = data["routine_id"]
        routine_obj = Routine.objects.get(id = routine_id)
        routine_obj.count +=1
        routine_obj.save()
        
        return Response({'response':True,'record_id':record_id}, status=status.HTTP_201_CREATED, headers=headers)
    #이미지 수정
    def partial_update(self,request,pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'response':True},status=status.HTTP_200_OK)
    
class ymMyRecordListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberForRoutineSerializer
    # queryset = Member.objects.all()

    def list(self,request):
        # queryset = get_queryset()
        queryset = Member.objects.filter(token =self.request.META.get('HTTP_AUTHORIZATION') )
        serializer = MemberForRecordSerializer(queryset, many=True)
        # print(serializer.data)
        data = serializer.data
        myres=[]
        for member in data:
            member_id = member['id']
            member_nickname = member['nickname']
            member_img = member['img']
            member_isOpen = member["isOpen"]
            for record_member in member['record_member']:
                #루틴 정보 조회
                routine_id = record_member["routine_id"]
                routine_obj = Routine.objects.get(id = routine_id)
                routine_id = routine_obj.id
                routine_name = routine_obj.routineName
                routine_isOpen = routine_obj.isOpen
                record_one = {}
                record_one["record_id"] = record_member["id"]
                record_one["record_comment"] = record_member["comment"]
                record_one["record_img"] = record_member["img"]
                record_one["record_start_time"] = record_member["start_time"]
                record_one["record_end_time"] = record_member["end_time"]
                record_one["record_create_time"] = record_member["create_time"]

                record_one["routine_id"] = routine_id
                record_one["routine_name"] = routine_name
                record_one["routine_isOpen"] = routine_isOpen
                record_one["member_id"] = member_id
                record_one["member_nickname"] = member_nickname
                record_one["member_img"] = member_img
                record_one["member_isOpen"] = member_isOpen
                myres.append(record_one)

        return Response(myres,status=status.HTTP_200_OK)


class ymFollowingRecordListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberForRoutineSerializer

#todo
    def list(self,request):
        member = Member.objects.get(token = self.request.META.get('HTTP_AUTHORIZATION'))
        q = Q(token =self.request.META.get('HTTP_AUTHORIZATION'))
        following_list = Follow.objects.filter(follower_id = member.id)
        for follow_obj in following_list:
            q.add(Q(id=follow_obj.following_id.id),q.OR)
        queryset = Member.objects.filter(q) 
        serializer = MemberForRecordSerializer(queryset, many=True)
        # print(serializer.data)
        data = serializer.data
        myres=[]
        for member in data:
            member_id = member['id']
            member_nickname = member['nickname']
            member_img = member['img']
            member_isOpen = member["isOpen"]
            for record_member in member['record_member']:
                #루틴 정보 조회
                routine_id = record_member["routine_id"]
                routine_obj = Routine.objects.get(id = routine_id)
                routine_id = routine_obj.id
                routine_name = routine_obj.routineName
                routine_isOpen = routine_obj.isOpen
                record_one = {}
                record_one["record_id"] = record_member["id"]
                record_one["record_comment"] = record_member["comment"]
                record_one["record_img"] = record_member["img"]
                record_one["record_start_time"] = record_member["start_time"]
                record_one["record_end_time"] = record_member["end_time"]
                record_one["record_create_time"] = record_member["create_time"]

                record_one["routine_id"] = routine_id
                record_one["routine_name"] = routine_name
                record_one["routine_isOpen"] = routine_isOpen
                record_one["member_id"] = member_id
                record_one["member_nickname"] = member_nickname
                record_one["member_img"] = member_img
                record_one["member_isOpen"] = member_isOpen
                myres.append(record_one)

        # print(myres)
        return Response(myres,status=status.HTTP_200_OK)

class RecordRoutineViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()

    def view_routineByRecord(self,request):
        member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
        records = self.queryset.filter(member_id = member.id)
        result = []
        for record in records:
            recordData = {}
            routine = record.routine_id
            routine_exercises = RoutineExercise.objects.filter(routine_id = routine.id)
            all_weight = 0
            for routine_exercise in routine_exercises:
                sets = Set.objects.filter(routine_exercise_id = routine_exercise.id)
                for set in sets:
                    all_weight += (set.count * set.weight)
            recordData['allWeight'] = all_weight
            recordData['time'] = record.create_time.strftime('%Y/%m/%d-%H:%M:%S')
            result.append(recordData)
        return Response(result,status=status.HTTP_200_OK)
