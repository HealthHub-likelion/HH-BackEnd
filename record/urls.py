from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import ymRecordViewSet,ymMyRecordListViewSet,ymFollowingRecordListViewSet,RecordRoutineViewSet, CommentViewset, ReplyCommentViewSet,RecordlikeViewSet
from django.conf.urls.static import static


#기록 리스트 조회/생성
record = ymRecordViewSet.as_view({
    'get':'list',
    'post': 'create',
})

#기록 수정=>(이미지 업로드) /삭제
#삭제 -> routine count 빼주기 todo
record_detail = ymRecordViewSet.as_view({
    'get':'retrieve',
    'delete': 'destroy',
    'post': 'partial_update'
})

#내 기록 예쁘게 조회
record_list = ymMyRecordListViewSet.as_view({
    'get':'list',
})
#팔로잉 기록 예쁘게 조회
record_list2 = ymFollowingRecordListViewSet.as_view({
    'get':'list',
})

recordByRoutine = RecordRoutineViewSet.as_view({
    'get':'view_routineByRecord'
})

commentByrecord = CommentViewset.as_view({
    'post' : 'create_comment',
    'delete' : 'delete_comment',
    'put' : 'update_comment'
})

recordLike = RecordlikeViewSet.as_view({
    'post' : 'likes'
})

replycommentByrecord = ReplyCommentViewSet.as_view({
    'post' : 'create_reply_comment',
    'delete' : 'delete_comment',
    'put' : 'update_comment'
})

urlpatterns =[
    path('',record),
    # path('img/',record_image),
    path('mylist/',record_list),
    path('followinglist/',record_list2),
    path('<int:pk>/',record_detail),
    path('<int:pk>/likes/',recordLike),
    path('routines',recordByRoutine),
    path('comment/', commentByrecord),
    path('reply_comment/', replycommentByrecord)
]