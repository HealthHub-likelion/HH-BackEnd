from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from rest_framework import viewsets


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
class JMemberViewSet(viewsets.ModelViewSet):
    lookup_field = 'nickname'
    queryset = Member.objects.filter(nickname = lookup_field)
    serializer_class = MemberSerializer