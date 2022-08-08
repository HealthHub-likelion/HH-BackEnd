from asyncio.windows_events import NULL
from urllib import response
from django.shortcuts import render
from itsdangerous import Serializer
from .models import Exercise,Routine,RoutineExercise,Set
from accounts.models import Member
from .serializers import ExerciseSerializer,RoutineSerializer,RoutineExerciseSerializer,SetSerializer,RoutineOnlySerializer,RoutineExerciseOnlySerializer
import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status


class ymExerciseList(generics.ListAPIView):
    serializer_class = ExerciseSerializer
    #운동 검색(부위별로)
    #http://127.0.0.1:8000/exercise/list?
    #http://127.0.0.1:8000/exercise/list?part=%ED%8C%94
    def get_queryset(self):
        queryset = Exercise.objects.all()
        searchpart = self.request.query_params.get('part')
        if searchpart is not None:
            queryset = queryset.filter(part=searchpart)
        return queryset

class ymExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()


class ymRoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    #루틴 리스트 예쁘게 전달
    def list(self, request):
        member = Member.objects.get(token =self.request.META.get('HTTP_AUTHORIZATION'))
        queryset = Routine.objects.filter(member_id = member) 
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        routine_idx = 0
        for routine in data:
            ex_list = routine["re_routine"]
            ex_idx = 0
            for exercise in ex_list:
                ex_obj = Exercise.objects.get(id = exercise["exercise_id"])
                ko_name = ex_obj.ko_name
                en_name = ex_obj.en_name
                data[routine_idx]["re_routine"][ex_idx]["exercise_ko_name"] = ko_name
                data[routine_idx]["re_routine"][ex_idx]["exercise_en_name"] = en_name
                ex_idx +=1
            routine_idx +=1
        print(data)

        return Response(data,status=status.HTTP_200_OK)


    #루틴 하나 예쁘게 전달
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        data = self.serializer_class(instance).data
        # print(self.serializer_class(instance).data)
        routine_list = data["re_routine"]
        idx = 0
        for routine in routine_list:
            ex_obj = Exercise.objects.get(id = routine["exercise_id"])
            ko_name = ex_obj.ko_name
            en_name = ex_obj.en_name
            data["re_routine"][idx]["exercise_ko_name"] = ko_name
            data["re_routine"][idx]["exercise_en_name"] = en_name
            idx +=1
        # print(data)
        return Response(data,status=status.HTTP_200_OK)

    #루틴 생성
    def create(self,request):
        data = json.loads(request.body)
        #멤버 정보
        member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
        #루틴 만들기
        new_routine = Routine.objects.create(
            member_id = member,
            creatorName = member.nickname,
            routineName = data['routineName'],
            isOpen = data['isOpen'],
            count = 0
        )

        #RoutineExercise 만들기
        exerciselist = data['ExerciseList']
        for exercise in exerciselist:
            ex_obj = Exercise.objects.get(ko_name = exercise['ko_name'])

            new_routine_exercise = RoutineExercise.objects.create(
                routine_id = new_routine,
                exercise_id = ex_obj
            )

            #Set 만들기
            setlist = exercise["set_list"]
            for set in setlist:
                new_set = Set.objects.create(
                    routine_exercise_id = new_routine_exercise,
                    count = set["count"],
                    weight = set['weight'],
                )
        
        return Response({'response':True},status=status.HTTP_200_OK)

    def update(self,request,pk):
        data = json.loads(request.body)
        #멤버 정보
        member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
        #기존 루틴 찾기
        routine_obj = Routine.objects.get(id = pk)

        #새 루틴 만들기
        new_routine = Routine.objects.create(
            member_id = member,
            creatorName = member.nickname,
            routineName = data['routineName'],
            isOpen = data['isOpen'],
            count = routine_obj.count #기존 루틴 카운트 그대로
        )

        #RoutineExercise 만들기
        exerciselist = data['ExerciseList']
        for exercise in exerciselist:
            ex_obj = Exercise.objects.get(ko_name = exercise['ko_name'])

            new_routine_exercise = RoutineExercise.objects.create(
                routine_id = new_routine,
                exercise_id = ex_obj
            )

            #Set 만들기
            setlist = exercise["set_list"]
            for set in setlist:
                new_set = Set.objects.create(
                    routine_exercise_id = new_routine_exercise,
                    count = set["count"],
                    weight = set['weight'],
                )

        #기존 루틴 멤버 연결 끊기
        routine_obj.member_id = None
        routine_obj.save()
        
        return Response({'response':True},status=status.HTTP_200_OK)





class ymRoutineDetailViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineOnlySerializer

    def partial_update(self,request,pk):
        data = json.loads(request.body)
        isopen = data['isOpen']
        if isopen == "True" or isopen == "False":
            routine = Routine.objects.get(id = pk)
            routine.isOpen = data['isOpen']
            routine.save()
            return Response({'response':True},status=status.HTTP_200_OK)
        else:
            return Response({'response':False},status=status.HTTP_200_OK)

class ymRoutineForkViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineOnlySerializer

    def update(self,request,pk):
        # data = json.loads(request.header)
        print(request.META.get('HTTP_AUTHORIZATION'))
        
        member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
        
        oriroutine = Routine.objects.get(id = pk)
        #루틴 복사
        newroutine = Routine.objects.create(
            member_id = member,#본인 
            creatorName = oriroutine.creatorName, #출처 닉네임
            routineName = oriroutine.routineName,
            count = 0,
            isOpen = True
        )
        re_obj_list = RoutineExercise.objects.filter(routine_id = pk)
        #루틴-운동 복사 / 세트 복사
        for re_obj in re_obj_list:
            ex_obj = Exercise.objects.get(id = re_obj.exercise_id.id)
            set_obj_list = Set.objects.filter(routine_exercise_id=re_obj.id)
            new_re_obj = RoutineExercise.objects.create(
                routine_id = newroutine,#새로운 루틴_id
                exercise_id = ex_obj#기존 운동_id
            )
            for set_obj in set_obj_list:
                new_set = Set.objects.create(
                    routine_exercise_id = new_re_obj,
                    count = set_obj.count,
                    weight = set_obj.weight
                )
        return Response({'response':True},status=status.HTTP_200_OK)     




class ymRoutineExerciseViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseOnlySerializer

class ymSetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer