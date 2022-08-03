from django.shortcuts import render
from .models import Exercise,Routine,RoutineExercise,Set
from accounts.models import Member
from .serializers import ExerciseSerializer,RoutineSerializer,RoutineExerciseSerializer,SetSerializer
import json
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status


class ymExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ymRoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

class ymRoutineDetailViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

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
    serializer_class = RoutineSerializer

    def update(self,request,pk):
        # data = json.loads(request.header)
        print(request.META.get('HTTP_TOKEN'))
        member = Member.objects.get(token = request.META.get('HTTP_TOKEN'))
        oriroutine = Routine.objects.get(id = pk)
        newroutine = Routine.objects.create(
            member_id = member,#본인 
            creatorName = oriroutine.creatorName, #출처 닉네임
            routineName = oriroutine.routineName,
            count = 0,
            isOpen = True
        )
        re_obj_list = RoutineExercise.objects.filter(routine_id = pk)
        for re_obj in re_obj_list:
            ex_obj = Exercise.objects.get(id = re_obj.exercise_id.id)

            new_re_obj = RoutineExercise.objects.create(
                routine_id = newroutine,#새로운 루틴_id
                exercise_id = ex_obj#기존 운동_id
            )
        return Response(True,status=status.HTTP_200_OK)


class ymRoutineExerciseViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseSerializer

class ymSetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer