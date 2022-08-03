from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import MemberViewSet

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('member', MemberViewSet)

member = MemberViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'delete': 'destroy',
})


urlpatterns =[
    path('', member),
]