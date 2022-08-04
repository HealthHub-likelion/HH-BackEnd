from .models import Member, Follow
from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields= ['nickname','email','password']

class MemberCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email','nickname']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Follow
        fields = ['following_id','follower_id']