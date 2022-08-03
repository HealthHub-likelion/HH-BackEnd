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

class MemberCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email','nickname']