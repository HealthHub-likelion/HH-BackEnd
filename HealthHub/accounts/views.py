from telnetlib import STATUS
from urllib.request import install_opener
from django.shortcuts import get_object_or_404, render
from .models import Member, Follow
from exercise.models import Routine
from record.models import Record
from .serializers import MemberSerializer, MemberCheckSerializer, FollowSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import secrets
import json

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberCheckViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberCheckSerializer

    def check_token(self,request):
        header = request.META.get('HTTP_AUTHORIZATION')
        member = get_object_or_404(self.queryset,token = header)
        routines = Routine.objects.filter(member_id=member.id)
        followers = Follow.objects.filter(following_id = member.id)
        followings = Follow.objects.filter(follower_id = member.id)
        records = Record.objects.filter(member_id=member.id)
        #이미지 경로를 url로 안보내고 그냥 값으로 보내면 decode 오류 발생!! 주의!!
        jsonData = {
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
            routine_data = {
                'routineId' : routine.id,
                'routineName' : routine.routineName,
                'routineCount' : routine.count,
                'routineOpen' : routine.isOpen
            }
            jsonData['routine'].append(routine_data)
        for record in records:
            jsonData['recordTimeList'].append(record.create_time.strftime('%Y/%m/%d'))
        
        return Response(jsonData,status=status.HTTP_200_OK)

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
        return Response({"token" : member.token},status=status.HTTP_200_OK)

class MemberFollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    m_queryset = Member.objects.all()
    serializer_class = FollowSerializer

    def follow_member(self,request):
        header = request.META['HTTP_AUTHORIZATION']
        name = request.data['name']
        following_member = get_object_or_404(self.m_queryset,nickname=name)
        member = get_object_or_404(self.m_queryset,token=header)
        Follow.objects.create(
            following_id = following_member,
            follower_id = member
        )
        return Response({'response':True},status=status.HTTP_200_OK)

    def unfollow_member(self, request):
        header = request.META['HTTP_AUTHORIZATION']
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

    def show_follow(self, request):
        query = request.GET.get('who', None)
        json = {'Member':[]}
        if query == 'follower':
            header = request.META.get('HTTP_AUTHORIZATION')
            member = get_object_or_404(self.m_queryset,token = header)
            follow_list = self.queryset.filter(following_id = member.id) 
            for follow in follow_list:
                follow_member = self.m_queryset.get(nickname=follow.follower_id)
                json['Member'].append({'name':follow_member.nickname,'img':follow_member.img.url})
        elif query == 'following':
            header = request.META.get('HTTP_AUTHORIZATION')
            member = get_object_or_404(self.m_queryset,token = header)
            follow_list = self.queryset.filter(follower_id = member.id) 
            for follow in follow_list:
                follow_member = self.m_queryset.get(nickname=follow.following_id)
                json['Member'].append({'name':follow_member.nickname,'img':follow_member.img.url})
        else:
            return Response({'response':False},status=status.HTTP_400_BAD_REQUEST)
        return Response(json,status=status.HTTP_200_OK)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer