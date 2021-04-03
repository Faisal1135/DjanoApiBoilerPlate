from collections import OrderedDict
import re
from django.contrib.auth import get_user, get_user_model
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Post
from core.serializer import PostSerializer


# Create your views here.
User = get_user_model()


class TestView(APIView):
    def get(self, req, *arg, **kwarg):
        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        resData = serializer.data

        for post in resData:
            post["owner"].pop('password')

        return Response(resData)

    def post(self, req, *arg, **kwarg):
        owner_id = req.data["owner"]
        parseUser = User.objects.get(pk=owner_id)
        if parseUser == None:
            return Response({"message": "Please enter a valid User"})

        parseFormData = req.data

        newpost = Post.objects.create(
            title=parseFormData["title"], description=parseFormData["description"], owner=parseUser)

        newserialzer = PostSerializer(newpost)

        return Response(newserialzer.data)
        # return Response({"error": "Somethon"})

        # print(serializer.data)
        # # serializer.save()
        # return Response(parseFormData)

    # def post(self, req, *arg, **kwarg):
    #     return Response({"name": 'galib', "age": 43})


# class PostView(APIView):
#       def get(self, req, *arg, **kwarg):


#     def post(self, req, *arg, **kwarg):
#         return Response({"name": 'galib', "age": 43})
