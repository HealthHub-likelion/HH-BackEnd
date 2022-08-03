from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer, MemberCheckSerializer, MemberSearchByNickname
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class JMemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSearchByNickname
    
    def search_nickname(self, request):
        print("\n\n\n", request.data, "\n\n\n")
        
        searched_member = Member.objects.get(nickname=request.data['nickname'])
        print(searched_member)
        
        if('nickname' in request.data):
            if(searched_member != None ):
                nickname = searched_member.get('nickname')
                img_path = searched_member.get('img')
                return Response({'Member':{
                    'name' : nickname,
                    'img' : img_path
                    }},status=status.HTTP_200_OK)
        else:
            return Response({'response':'유효하지 않은 인자가 요청되었습니다.'},status = status.HTTP_400_BAD_REQUEST)
    
    
    
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