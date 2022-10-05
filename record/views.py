from urllib import response
from django.shortcuts import render,get_object_or_404
from itsdangerous import Serializer

from exercise.models import Routine, RoutineExercise, Set
from .models import Record
from accounts.models import Member,Follow
from .serializers import RecordSerializer,MemberForRecordSerializer
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q
import datetime

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
        mem_id = data["member_id"]
        mem_obj = Member.objects.get(id = mem_id)
        #타임리스트 생성
        records = Record.objects.filter(member_id=mem_id)
        recordTimeList = []
        for record in records:
            recordTimeList.append(record.create_time.strftime('%Y/%m/%d'))

        # #파도 레벨
        # print(recordTimeList)
        # continue_day = 0
        # decreaseCount = 0
        # wave_level = 0
        # for i in range (29,-1,-1):
        #     tempdate = datetime.date.today()-datetime.timedelta(days=i)
        #     tempdate = tempdate.strftime('%Y/%m/%d')
        #     # print("tempdate:",tempdate)

        #     if(recordTimeList):
        #         if tempdate in recordTimeList:
        #             if continue_day < 3:continue_day+=1
        #             decreaseCount=0
        #             wave_level+=1
        #         else:
        #             continue_day = 0
        #             decreaseCount +=1
        #             if decreaseCount >= 7:
        #                 if wave_level >0: 
        #                     wave_level -1
        #                 decreaseCount = 0

        # # print("wave_level",wave_level)
        # mem_obj.level = wave_level

        # #연속일수 구하기
        # record_day = 0
        # idx = 0
        # while True:
        #     tempdate = datetime.date.today()-datetime.timedelta(days=idx)#오늘부터 하루씩 뒤로
        #     tempdate = tempdate.strftime('%Y/%m/%d')
        #     if tempdate in recordTimeList:
        #         record_day +=1
        #         idx +=1
        #     else:
        #         break
        # # print("record_day",record_day)
        # mem_obj.record_day = record_day
        # mem_obj.save()
        


        #member record_day update

        return Response({'response':True,'record_id':record_id}, status=status.HTTP_201_CREATED, headers=headers)
    #이미지 수정
    def partial_update(self,request,pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'response':True},status=status.HTTP_200_OK)
    
    # 레벨 갱신
    def level_update():
        return

    #연속일수 갱신
    def record_day_update():
        return

    
class ymMyRecordListViewSet(viewsets.ModelViewSet):
    serializer_class = MemberForRecordSerializer
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
    serializer_class = MemberForRecordSerializer

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
