from urllib import response
from django.shortcuts import render
from .models import Exercise,Routine,RoutineExercise,Set
from accounts.models import Member
from .serializers import ExerciseSerializer,RoutineSerializer,RoutineExerciseSerializer,SetSerializer,RoutineOnlySerializer,RoutineExerciseOnlySerializer
import json
# Create your views here.
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
    serializer_class = RoutineOnlySerializer

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
            return Response(True,status=status.HTTP_200_OK)
        else:
            return Response(False,status=status.HTTP_200_OK)

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
            ex_obj = Exercise.objects.get(id = re_obj.exercise_name.id)
            set_obj_list = Set.objects.filter(routine_exercise_id=re_obj.id)
            new_re_obj = RoutineExercise.objects.create(
                routine_id = newroutine,#새로운 루틴_id
                exercise_name = ex_obj#기존 운동_name
            )
            for set_obj in set_obj_list:
                new_set = Set.objects.create(
                    routine_exercise_id = new_re_obj,
                    count = set_obj.count,
                    weight = set_obj.weight
                )
        return Response(True,status=status.HTTP_200_OK)     




class ymRoutineExerciseViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseOnlySerializer

class ymSetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer