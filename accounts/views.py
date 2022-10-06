from ast import arg
import stat
import re
import bcrypt
from .pagination import RankingPagination
from telnetlib import STATUS
from urllib.request import install_opener
from xmlrpc.client import ResponseError
from django.shortcuts import get_object_or_404, render
from .models import Member, Follow
from exercise.models import Routine
from record.models import Record
from .serializers import MemberSerializer, MemberCheckSerializer, FollowSerializer, MemberSearchByNicknameSerializer, MemberUpdateReadmeSerializer, MemberUploadProfileImageSerializer, MemberGetTokenSerializer,MemberRankingeSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
import secrets
import json
import datetime

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create_member(self,request):
        password = request.data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        decode_password = hashed_password.decode('utf-8')
        
        Member.objects.create(
            email = request.data['email'],
            nickname = request.data['name'],
            password = decode_password,
            img = 'images/HH_logo.jpg'
        )
        return Response({'response':True},status=status.HTTP_200_OK)
    #닉네임 수정
    def partial_update(self,request,pk):
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'response':True},status=status.HTTP_200_OK)




class MemberCheckViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberCheckSerializer

    def view_member(self,request):
        param = request.GET.get('name', None)
        header = request.META.get('HTTP_AUTHORIZATION')
        member = self.queryset.filter(token = header)
        find_member = get_object_or_404(self.queryset,nickname=param)
        routines = Routine.objects.filter(member_id=find_member.id)
        followers = Follow.objects.filter(following_id = find_member.id)
        followings = Follow.objects.filter(follower_id = find_member.id)
        records = Record.objects.filter(member_id=find_member.id)
        args = {'find_member':find_member,'routines':routines,'followers':followers,'followings':followings ,'records':records}

        #토큰 유효
        if member.count() > 0:
            #자기 페이지 조회
            if member.first().id == find_member.id:
                return Response(self.make_jsonData(True,None,args),status=status.HTTP_200_OK)
            else:
                isFollow = followers.filter(follower_id = member.first().id).count() > 0
                if find_member.isOpen: #다른 사용자 페이지 공개인경우
                    return Response(self.make_jsonData(True,isFollow,args),status=status.HTTP_200_OK)
                else: # 다른 사용자 페이지 비공개
                    return Response(self.make_jsonData(False,isFollow,args),status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

    def make_jsonData(self,isPublic,isFollow,args):
        if isPublic:
            #이미지 경로를 url로 안보내고 그냥 값으로 보내면 decode 오류 발생!! 주의!!
            jsonData = {
                'id':args['find_member'].id,
                'name':args['find_member'].nickname,
                'img':args['find_member'].img.url,
                'followerCount':args['followers'].count(),
                'followingCount':args['followings'].count(),
                'readMe':args['find_member'].readMe,
                'routine':[],
                'recordCount':args['records'].count(),
                'recordTimeList':[],
                'isFollow': isFollow,
                'isOpen':True
            }
            for routine in args['routines']:
                recentRoutine = Record.objects.filter(member_id=args['find_member'].id,routine_id=routine.id)
                if recentRoutine.exists():
                    time = recentRoutine[0].create_time.strftime('%Y/%m/%d-%H:%M:%S')
                else:
                    time = None
                routine_data = {
                    'routineId' : routine.id,
                    'routineName' : routine.routineName,
                    'routineCount' : routine.count,
                    'routineOpen' : routine.isOpen,
                    'recentRoutine' : time
                }
                jsonData['routine'].append(routine_data)
            for record in args['records']:
                jsonData['recordTimeList'].append(record.create_time.strftime('%Y-%m-%d'))
        else:
            jsonData = {
                'img' : args['find_member'].img.url,
                'followerCount':args['followers'].count(),
                'followingCount':args['followings'].count(),
                'isFollow':isFollow,
                'isOpen' : False
            }
        return jsonData


    def check_member(self,request):
        if('name' in request.data):
            if Member.objects.filter(nickname=request.data['name']).count() == 0:
                return Response({'response':True},status=status.HTTP_200_OK)
            else:
                return Response({'response':False},status = status.HTTP_400_BAD_REQUEST)

        elif('email' in request.data):
            if Member.objects.filter(email=request.data['email']).count() == 0:
                return Response({'response':True},status=status.HTTP_200_OK)
            else:
                return Response({'response':False},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'response':'유효하지 않은 인자가 요청되었습니다.'},status = status.HTTP_400_BAD_REQUEST)
        
    def open_member(self, request):
        header = request.META['HTTP_AUTHORIZATION']
        member = get_object_or_404(self.queryset,token=header)
        if member:
            is_open = request.data['isOpen']
            member.isOpen = is_open
            member.save()
            return Response({'response':True},status=status.HTTP_200_OK)
        else:
            Response({'response':False},status=status.HTTP_400_BAD_REQUEST)
    
    def delete_member(self, request):
        header = request.META['HTTP_AUTHORIZATION']
        member = get_object_or_404(self.queryset,token=header)
        if member:
            member.delete()
            return Response({'response':True},status=status.HTTP_200_OK)
        else:
            Response({'response':False},status=status.HTTP_400_BAD_REQUEST)

class MemberSessionViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberCheckSerializer

    def login(self, request):
        member = Member.objects.get(password = request.data['password'],email=request.data['email'])
        member.token = secrets.token_urlsafe(30)
        member.save()
        return Response({"token" : member.token, "name":member.nickname},status=status.HTTP_200_OK)

    def check_token(self,request):
        header = request.META.get('HTTP_AUTHORIZATION')
        member = get_object_or_404(self.queryset,token = header)
        routines = Routine.objects.filter(member_id=member.id)
        followers = Follow.objects.filter(following_id = member.id)
        followings = Follow.objects.filter(follower_id = member.id)
        records = Record.objects.filter(member_id=member.id)
        #이미지 경로를 url로 안보내고 그냥 값으로 보내면 decode 오류 발생!! 주의!!
        jsonData = {
            'id':member.id,
            'name':member.nickname,
            'img':member.img.url,
            'followerCount':followers.count(),
            'followingCount':followings.count(),
            'readMe':member.readMe,
            'routine':[],
            'recordCount':records.count(),
            'recordTimeList':[]
        }
        for routine in routines:
            recentRoutine = Record.objects.filter(member_id=member.id,routine_id=routine.id)
            if recentRoutine.exists():
                time = recentRoutine[0].create_time.strftime('%Y/%m/%d-%H:%M:%S')
            else:
                time = None

            routine_data = {
                'routineId' : routine.id,
                'routineName' : routine.routineName,
                'routineCount' : routine.count,
                'routineOpen' : routine.isOpen,
                'recentRoutine' : time
            }
            jsonData['routine'].append(routine_data)
        for record in records:
            jsonData['recordTimeList'].append(record.create_time.strftime('%Y/%m/%d'))
        
        return Response(jsonData,status=status.HTTP_200_OK)

class MemberFollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    m_queryset = Member.objects.all()
    serializer_class = FollowSerializer

    def follow_member(self,request):
        header = request.META['HTTP_AUTHORIZATION']
        name = request.data['name']
        following_member = get_object_or_404(self.m_queryset,nickname=name)
        member = get_object_or_404(self.m_queryset,token=header)
        if not Follow.objects.filter(following_id = following_member.id, follower_id = member.id).exists():
            Follow.objects.create(
                following_id = following_member,
                follower_id = member
            )
        return Response({'response':True},status=status.HTTP_200_OK)

    def show_follow(self, request):
        query = request.GET.get('who', None)
        nickname = request.GET.get('name')
        json = {'Member':[]}
        if query == 'follower':
            header = request.META.get('HTTP_AUTHORIZATION')
            member = get_object_or_404(self.m_queryset,nickname = nickname)
            follow_list = self.queryset.filter(following_id = member.id) 
            for follow in follow_list:
                follow_member = self.m_queryset.get(nickname=follow.follower_id)
                isFollow = self.queryset.filter(following_id = follow_member.id, follower_id = member.id).exists()
                json['Member'].append({'id':follow.id,'name':follow_member.nickname,'img':follow_member.img.url,'isFollow':isFollow})
        elif query == 'following':
            header = request.META.get('HTTP_AUTHORIZATION')
            member = get_object_or_404(self.m_queryset,nickname = nickname)
            follow_list = self.queryset.filter(follower_id = member.id) 
            for follow in follow_list:
                follow_member = self.m_queryset.get(nickname=follow.following_id)
                json['Member'].append({'id':follow.id,'name':follow_member.nickname,'img':follow_member.img.url,'isFollow':True})
        else:
            return Response({'response':False},status=status.HTTP_400_BAD_REQUEST)
        return Response(json,status=status.HTTP_200_OK)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    m_queryset = Member.objects.all()

    def unfollow_member(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        name = request.data['name']
        following_member = get_object_or_404(self.m_queryset,nickname=name)
        member = get_object_or_404(self.m_queryset,token=header)
        follow_data = get_object_or_404(
                            self.queryset,
                            following_id=following_member,
                            follower_id = member
                        )
        follow_data.delete()
        return Response({'response':True},status=status.HTTP_200_OK)


    
class MemberSearchByNicknameViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSearchByNicknameSerializer
    
    def search_nickname(self, request):
        
        searched_member = Member.objects.get(nickname=request.data['nickname'])
        print(searched_member)
        
        if('nickname' in request.data):
            if(searched_member != None ):
                nickname = searched_member.nickname
                img_path = str(searched_member.img)
                return Response({'Member':{
                    'name' : nickname,
                    'img' : img_path
                    }},status=status.HTTP_200_OK)
        else:
            return Response({'response':'유효하지 않은 인자가 요청되었습니다.'},status = status.HTTP_400_BAD_REQUEST)
        


#31
class MemberUpdateReadmeViewSet(viewsets.ModelViewSet):
    serializer_class = MemberUpdateReadmeSerializer
    def update_readme(self, request):
        try:
            member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
            member.readMe = request.data['readMe']
            member.save()
            return Response({'response':True},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)




#44
class MemberGetSettingOption(viewsets.ModelViewSet):
    serializer_class = MemberGetTokenSerializer
    def get_setting_option(self, request):
        try:
            member = Member.objects.get(token = request.META.get('HTTP_AUTHORIZATION'))
            img = str(member.img)
            nickname = member.nickname
            isOpen = member.isOpen
            data = {'status' : { 'image' : {img}, 'name' : {nickname}, 'isOpen' : {isOpen} }}
            
            return Response(data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)
            

#45
class MemberUploadProfileImage(viewsets.ModelViewSet):
    serializer_class = MemberUploadProfileImageSerializer
    def upload_profile_image(self, request):
        try:            
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            member.img = request.data['img']
            member.save()
            return Response({'response' : 'https://hh-image-storage.s3.ap-northeast-2.amazonaws.com/' + str(member.img)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)
    
    def delete_profile_image(self, request):
        try:
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            member.img = ""
            member.save()
            return Response({'response' : True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)

#46
class MemberDeleteProfileImage(viewsets.ModelViewSet):
    serializer_class = MemberGetTokenSerializer
    def delete_profile_image(self, request):
        try:
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            file_path = str(member.img)
            member.img = "images/HH_logo.jpg"
            member.save()
            return Response({'response' : True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)
        
        
#52-2
class MemberSearchByKeyword(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    def search_by_keyword(self, request):
        try:
            keyword = request.data['keyword']
            dict_data = {'Member':[]}
            members = Member.objects.all()
            for member in members:
                if keyword in member.nickname:
                    dict_data['Member'].append({'name':member.nickname,'img':str(member.img)})
            
            json_data = json.dumps(dict_data)
            
            #return Response(json_data,status=status.HTTP_200_OK)
            return Response(dict_data,status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'response' : False}, status.HTTP_400_BAD_REQUEST)

#랭킹(멤버 리스트 정렬):
class MemberRankingViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberRankingeSerializer
    pagination_class = RankingPagination
    filter_backends = [filters.OrderingFilter] 
    # ordering_fields = ['-level','-record_day'] 
    ordering = ['-level','-record_day']

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     # print(serializer.data)
    #     return Response(serializer.data)

def check():
    #모든 멤버에 대해서
    memberlist = Member.objects.all()
    print(memberlist)
    for mem_obj in memberlist:
        records = Record.objects.filter(member_id=mem_obj.id)
        recordTimeList = []
        for record in records:
            recordTimeList.append(record.create_time.strftime('%Y/%m/%d'))

        #파도 레벨
        print(recordTimeList)
        continue_day = 0
        decreaseCount = 0
        wave_level = 0
        for i in range (29,-1,-1):
            tempdate = datetime.date.today()-datetime.timedelta(days=i)
            tempdate = tempdate.strftime('%Y/%m/%d')
            # print("tempdate:",tempdate)

            if(recordTimeList):
                if tempdate in recordTimeList:
                    if continue_day < 3:continue_day+=1
                    decreaseCount=0
                    wave_level+=1
                else:
                    continue_day = 0
                    decreaseCount +=1
                    if decreaseCount >= 7:
                        if wave_level >0: 
                            wave_level -1
                        decreaseCount = 0

        # print("wave_level",wave_level)
        mem_obj.level = wave_level

        #연속일수 구하기
        record_day = 0
        idx = 0
        while True:
            tempdate = datetime.date.today()-datetime.timedelta(days=idx)#오늘부터 하루씩 뒤로
            tempdate = tempdate.strftime('%Y/%m/%d')
            if tempdate in recordTimeList:
                record_day +=1
                idx +=1
            else:
                break
        # print("record_day",record_day)
        mem_obj.record_day = record_day
        mem_obj.save()

    print("동작 완료")
