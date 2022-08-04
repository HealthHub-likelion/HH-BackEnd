from dataclasses import field

from .models import Member
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields= '__all__'
        
class MemberSearchByNickname(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields= ['nickname']
        
class MemberUpdateReadme(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['token', 'readMe']
        
class MemberUploadProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['token', 'img']
        
class MemberDeleteProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['token']
        
        

class MemberCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email','nickname']