from django.shortcuts import render
from .models import Exercise,Routine,RoutineExercise,Set
from .serializers import ExerciseSerializer,RoutineSerializer,RoutineExerciseSerializer,SetSerializer

# Create your views here.
from rest_framework import viewsets


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

class RoutineExerciseViewSet(viewsets.ModelViewSet):
    queryset = RoutineExercise.objects.all()
    serializer_class = RoutineExerciseSerializer

class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer