from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from auths.serializers import UserSerializerAll
from auths.paginators import MyLimitPaginator


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = MyLimitPaginator
    serializer_class = UserSerializerAll
