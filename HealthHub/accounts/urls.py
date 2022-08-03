from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import MemberViewSet, JMemberViewSet, MemberCheckViewSet

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

j_member_search_by_nickname = JMemberViewSet.as_view({
    'get': 'retrieve',
})

member_check = MemberCheckViewSet.as_view({
    'post': 'check_member'
})


urlpatterns =[
    path('', member_list),
    path('<int:pk>', j_member_detail),
    path('checkNickName/<str:nickname>', j_member_search_by_nickname),
    path('member/',member_check)
]