from urllib import response
from django.shortcuts import render
from itsdangerous import Serializer

from exercise.models import Routine
from .models import Record
from accounts.models import Member,Follow
from .serializers import RecordSerializer,MemberForRoutineSerializer
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

        #루틴 count 올려주기
        # data = json.loads(data)
        # print(data)
        routine_id = data["routine_id"]
        routine_obj = Routine.objects.get(id = routine_id)
        routine_obj.count +=1
        routine_obj.save()
        
        return Response({'response':True}, status=status.HTTP_201_CREATED, headers=headers)
    
class ymMyRecordListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberForRoutineSerializer
    # queryset = Member.objects.all()


    def list(self,request):
        # queryset = get_queryset()
        queryset = Member.objects.filter(token =self.request.META.get('HTTP_AUTHORIZATION') )
        serializer = MemberForRoutineSerializer(queryset, many=True)
        # print(serializer.data)
        data = serializer.data
        myres=[]
        for member in data:
            member_id = member['id']
            member_nickname = member['nickname']
            member_img = member['img']
            member_isOpen = member["isOpen"]
            for routine in member['routine_member']:
                routine_id = routine["id"]
                routine_name = routine["routineName"]
                routine_isOpen = routine["isOpen"]
                for record in routine["record_routine"]:
                    record_one = {}
                    record_one["record_id"] = record["id"]
                    record_one["record_comment"] = record["comment"]
                    record_one["record_img"] = record["img"]
                    record_one["record_start_time"] = record["start_time"]
                    record_one["record_end_time"] = record["end_time"]
                    record_one["record_create_time"] = record["create_time"]
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


class ymFollowingRecordListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberForRoutineSerializer


    def list(self,request):
        member = Member.objects.get(token = self.request.META.get('HTTP_AUTHORIZATION'))
        q = Q(token =self.request.META.get('HTTP_AUTHORIZATION'))
        following_list = Follow.objects.filter(follower_id = member.id)
        for follow_obj in following_list:
            q.add(Q(id=follow_obj.following_id.id),q.OR)
        queryset = Member.objects.filter(q) 
        serializer = MemberForRoutineSerializer(queryset, many=True)
        # print(serializer.data)
        data = serializer.data
        myres=[]
        for member in data:
            member_id = member['id']
            member_nickname = member['nickname']
            member_img = member['img']
            for routine in member['routine_member']:
                routine_id = routine["id"]
                routine_name = routine["routineName"]
                for record in routine["record_routine"]:
                    record_one = {}
                    record_one["record_id"] = record["id"]
                    record_one["record_comment"] = record["comment"]
                    record_one["record_img"] = record["img"]
                    record_one["record_start_time"] = record["start_time"]
                    record_one["record_end_time"] = record["end_time"]
                    record_one["record_create_time"] = record["create_time"]
                    record_one["routine_id"] = routine_id
                    record_one["routine_name"] = routine_name
                    record_one["member_id"] = member_id
                    record_one["member_nickname"] = member_nickname
                    record_one["member_img"] = member_img
                    myres.append(record_one)

        # print(myres)
        return Response(myres,status=status.HTTP_200_OK)
