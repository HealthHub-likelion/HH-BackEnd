from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer, MemberCheckSerializer
from rest_framework import viewsets


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class JMemberViewSet(viewsets.ModelViewSet):
    lookup_field = 'nickname'
    queryset = Member.objects.filter(nickname = lookup_field)
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