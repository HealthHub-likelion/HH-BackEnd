from .models import Member, Follow
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields= ['nickname','email','password','img']

class MemberCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email','nickname']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Follow
        fields = ['following_id','follower_id']
        
class MemberSearchByNicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['nickname']
        
class MemberUpdateReadmeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['readMe']
        
class MemberGetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['nickname', 'img', 'email']
        
class MemberUploadProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['img']

class MemberRankingeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields =['id','nickname','level','record_day']#img 추가?
        
