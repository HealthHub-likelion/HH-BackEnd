from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import MemberViewSet, JMemberViewSet

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('member', MemberViewSet)

member_list = MemberViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

j_member_detail = JMemberViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})


urlpatterns =[
    path('', member_list),
    path('<int:pk>', j_member_detail),
]