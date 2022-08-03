from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import ExerciseViewSet,RoutineViewSet,RoutineExerciseViewSet,SetViewSet

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('exercise', ExerciseViewSet)

exercise = ExerciseViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

routine = RoutineViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns =[
    path('', exercise),
    path('routines/', routine),
]