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
        fields = ['readMe']
        
class MemberUploadProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['img']
        
class MemberGetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = None
        
class MemberCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email','nickname']