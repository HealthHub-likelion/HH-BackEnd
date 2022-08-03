from django.shortcuts import render
from .models import Member
from .serializers import MemberSerializer
from rest_framework import viewsets


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer