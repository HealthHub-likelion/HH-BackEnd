from telnetlib import STATUS
from urllib.request import install_opener
from django.shortcuts import get_object_or_404, render
from .models import Member
from exercise.models import Routine
from .serializers import MemberSerializer, MemberCheckSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import secrets

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberCheckViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberCheckSerializer

    def check_member(self,request):
        print(request.data)

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