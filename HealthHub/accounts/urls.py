from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.urls import path, include
from .views import MemberGetSettingOption, MemberViewSet, MemberSearchByNickname, MemberCheckViewSet, MemberUpdateReadmeViewSet, MemberUploadProfileImage, MemberDeleteProfileImage

router = DefaultRouter()
# 첫 번째 인자는 url의 prefix
# 두 번째 인자는 ViewSet
router.register('member', MemberViewSet)

member_list = MemberViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

member_search_by_nickname = MemberSearchByNickname.as_view({
    'post': 'search_nickname',
})

member_check = MemberCheckViewSet.as_view({
    'post': 'check_member'
})

member_update_readme = MemberUpdateReadmeViewSet.as_view({
    'post': 'update_readme'
})

member_upload_profile_image = MemberUploadProfileImage.as_view({
    'post': 'upload_profile_image'
})

member_delete_profile_image = MemberDeleteProfileImage.as_view({
    'post': 'delete_profile_image'
})

member_get_setting_option = MemberGetSettingOption.as_view({
    'get' : 'get_setting_option'
})


urlpatterns =[
    path('', member_list),
    path('checknickname/', member_search_by_nickname),
    path('updatereadme/', member_update_readme),
    path('member/', member_check),
    path('profileimage/upload/', member_upload_profile_image),
    path('profileimage/delete/', member_delete_profile_image),
    path('getsettingoption/', member_get_setting_option),
]