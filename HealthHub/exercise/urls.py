from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import ymExerciseList,ymRoutineViewSet,ymRoutineExerciseViewSet,ymSetViewSet,ymRoutineDetailViewSet,ymRoutineForkViewSet,RoutineSerializer,ymExerciseViewSet

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
# router.register('exercise', ymExerciseList)
router.register('exercise', ymExerciseViewSet)
router.register('exercise', ymRoutineViewSet)
router.register('exercise', ymRoutineDetailViewSet)

exercise = ymExerciseViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})
#루틴 목록 조회/생성
routine_list = ymRoutineViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

# 루틴 조회/삭제
routine_detail = ymRoutineDetailViewSet.as_view({
    'get': 'retrieve',# todo 루틴 하나 보여줌. -> 운동 목록과 함께 보여주게
    'delete': 'destroy',
    'post': 'partial_update',#루틴 퍼블릭/프라이빗 요청
})

#루틴 fork
routine_fork = ymRoutineForkViewSet.as_view({
    'post':'update',
})





re = ymRoutineExerciseViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

set = ymSetViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns =[
    path('',exercise),
    path('list', ymExerciseList.as_view()),
    path('routine/',routine_list),
    path('routine/<int:pk>', routine_detail),
    path('routine/<int:pk>/fork', routine_fork),
    path('re/', re),
    path('set/', set),
]