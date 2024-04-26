import json

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes

from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# 视图：注册
class Register(APIView):
    def post(self, request):
        # 解析JSON数据
        data = json.loads(request.body.decode('utf-8'))
        # 提取用户注册信息
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        age = data.get('age')
        institute = data.get('institute')
        title = data.get('title')
        homepage_link = data.get('homepage_link')
        email = data.get('email')
        # 存储到数据库
        user = User(username=username, gender=gender, age=age, institute=institute, title=title,
                    homepage_link=homepage_link, email=email)
        user.set_password(password)
        user.save()
        # 注册成功
        return Response({'message': '用户注册成功'})


# 视图：用户资料
class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        profile = {
            'username': user.username,
            'gender': user.gender,
            'age': user.age,
            'institute': user.institute,
            'title': user.title,
            'homepage_link': user.homepage_link,
            'email': user.email,
        }
        return Response(profile)

