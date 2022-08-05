from urllib import response
from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer, MemberCheckSerializer, MemberSearchByNickname, MemberUpdateReadme, MemberUploadProfileImageSerializer, MemberGetTokenSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
import json


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer




class MemberSearchByNickname(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSearchByNickname
    
    def search_nickname(self, request):
        print("\n\n\n", request.data, "\n\n\n")
        
        searched_member = Member.objects.get(nickname=request.data['nickname'])
        print(searched_member)
        
        if('nickname' in request.data):
            if(searched_member != None ):
                nickname = searched_member.nickname
                img_path = str(searched_member.img)
                
                print("\n\n\n\n\n",img_path, " \n\n\n\n\n\n")
                return Response({'Member':{
                    'name' : nickname,
                    'img' : img_path
                    }},status=status.HTTP_200_OK)
        else:
            return Response({'response':'유효하지 않은 인자가 요청되었습니다.'},status = status.HTTP_400_BAD_REQUEST)
        


#31
class MemberUpdateReadmeViewSet(viewsets.ModelViewSet):
    serializer_class = MemberUpdateReadme
    def update_readme(self, request):
        try:
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            member.readMe = request.data['readMe']
            member.save()
            return Response({'response':True},status=status.HTTP_200_OK)
        except Exception as e:
            print("\n\n\n", e, "\n\n\n")
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
            
            print("\n\n\n전송 완료\n\n\n")
            
            
            data = {'status' : { 'image' : {img}, 'name' : {nickname}, 'isOpen' : {isOpen} }}
            print("data : ",type(data))
            print(data)
            
            return Response(data, status = status.HTTP_200_OK)
        except Exception as e:
            print("\n\n\n", e, "\n\n\n")
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)
            




#45
class MemberUploadProfileImage(viewsets.ModelViewSet):
    serializer_class = MemberUploadProfileImageSerializer
    def upload_profile_image(self, request):
        try:            
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            member.img = request.data['img']
            member.save()
            return Response({'response' : True}, status=status.HTTP_200_OK)
        except Exception as e:
            print("\n\n\n", e, "\n\n\n")
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)



#46
class MemberDeleteProfileImage(viewsets.ModelViewSet):
    serializer_class = MemberGetTokenSerializer
    def delete_profile_image(self, request):
        try:
            member = Member.objects.get(token=request.META.get('HTTP_AUTHORIZATION'))
            member.img = ""
            member.save()
            return Response({'response' : True}, status=status.HTTP_200_OK)
        except Exception as e:
            print("\n\n\n", e, "\n\n\n")
            return Response({'response':False},status.HTTP_400_BAD_REQUEST)
    
    
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