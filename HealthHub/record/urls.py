from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import ymRecordViewSet,ymMyRecordListViewSet,ymFollowingRecordListViewSet
from django.conf.urls.static import static


#기록 리스트 조회/생성
record = ymRecordViewSet.as_view({
    'get':'list',
    'post': 'create',
})

record_list = ymMyRecordListViewSet.as_view({
    'get':'list',
})
record_list2 = ymFollowingRecordListViewSet.as_view({
    'get':'list',
})

urlpatterns =[
    path('',record),
    path('mylist/',record_list),
    path('followinglist/',record_list2),
    
]