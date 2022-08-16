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
})
#루틴 목록 조회/생성
routine_list = ymRoutineViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

#루틴 한번에 수정
routin_one = ymRoutineViewSet.as_view({
    'get': 'retrieve',
    'post': 'update',
})

# 루틴 삭제
# 루틴 이름과 권한만 수정
routine_detail = ymRoutineDetailViewSet.as_view({
    'delete': 'destroy',
    'post': 'partial_update',#루틴 퍼블릭/프라이빗 요청
})

#루틴 fork
routine_fork = ymRoutineForkViewSet.as_view({
    'post':'update',
})

#루틴 이름 비교 
routine_compare = ymRoutineViewSet.as_view({
    'post': 'compare',
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
    path('list/', ymExerciseList.as_view()),
    path('routine/',routine_list),
    path('routine/<int:pk>/detail/', routine_detail),
    path('routine/<int:pk>/', routin_one),
    path('routine/<int:pk>/fork/', routine_fork),
    path('routine/compare/', routine_compare),
    path('re/', re),
    path('set/', set),
]