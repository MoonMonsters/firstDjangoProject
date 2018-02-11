
#encoding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from . import serializers

from haveFun import models
from django.http import HttpResponse
import json
from rest_framework  import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from haveFun.permissions import IsOwnerOrReadOnly
from PIL import Image
from io import StringIO
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import generics
import pymysql

from rest_framework import mixins

import os

def delete_image_file(file_path):
    '''
    删除文件
    '''
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        if os.path.isfile(file_full_path):
            #return file_full_path
            os.remove(file_full_path)


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)



class imageAPI(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = models.userHeadImage.objects.all()
    serializer_class = serializers.ImageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        user_id = data['user_id']
        m = models.userHeadImage.objects.filter(uploaded_by__exact=user_id)
        for model in m:
            model.image.delete()
            print(model.image)
            model.delete()
        try:
            self.create(request, *args, **kwargs)
            image = models.userHeadImage.objects.get(uploaded_by__exact=user_id)
            return JSONResponse({'result':serializers.ImageSerializer(image).data,'desc':'upload success'}, status=HTTP_200_OK)
        except:
            return JSONResponse({'desc':'upload faile'},status=HTTP_400_BAD_REQUEST)

class articalImageAPI(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    # queryset = models.userHeadImage.objects.all()
    # serializer_class = serializers.ImageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        filename = data['filename']
        m = models.articalHeadImage.objects.filter(filename__exact=filename)
        for model in m:
            model.image.delete()
            print(model.image)
            model.delete()
        try:
            return self.create(request, *args, **kwargs)
            image = models.articalHeadImage.objects.get(filename__exact=filename)
            return JSONResponse({'result':serializers.ImageSerializer(image).data,'desc':'upload success'}, status=HTTP_200_OK)
        except:
            return JSONResponse({'desc':'upload faile'},status=HTTP_400_BAD_REQUEST)

class UploadArticalImageSet(articalImageAPI):
    queryset = models.articalHeadImage.objects.all()
    serializer_class = serializers.ArticalImageSerializer
    parser_classes = (MultiPartParser, )    


class UploadViewSet(imageAPI):
    queryset = models.userHeadImage.objects.all()
    serializer_class = serializers.ImageSerializer
    parser_classes = (MultiPartParser, )

#分页
def api_paging(objs, request, Ser):
    page_size = int(request.POST.get('page_size'))
    page = int(request.POST.get('page'))
    print(type(objs))
    paginator=Paginator(objs,page_size,3) # paginator对象
    total = paginator.num_pages #总页数
    if(total<page):
      return JSONResponse({
        'result': [],
        'total': total,
        'page':page,
        'desc':'page success'
    }, status=HTTP_200_OK)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    serializer = Ser(p, many=True) #序列化操作
    print(len(serializer.data),'page=',page)
    return JSONResponse({
        'result': serializer.data,
        'total': total,
        'page':page,
        'desc':'page success'
    }, status=HTTP_200_OK) #返回


#用于登录

class UserLoginAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserInforSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       password = data.get('passwd')
       if not models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':'用户名不存在'},status=HTTP_200_OK,)
       user = models.haveFunUser.objects.get(name__exact=username)
       if user.passwd == password:
           serializer = serializers.UserInforSerializer(user)
           new_data = serializer.data
           print(new_data)
           # 记忆已登录用户
           self.request.session['user_id'] = user.user_id
           self.request.session['user_name'] = user.name
           return JSONResponse({'result':serializer.data,'desc':'登陆成功'}, status=HTTP_200_OK)
       return JSONResponse( {'desc':'password error'},status=HTTP_400_BAD_REQUEST)

#用于注册

class UserRegisterAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserInforSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       phone = data.get('phone')
       print('registrt--->',data)
       dic = {}
       if models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':'用户名已存在'},status=HTTP_400_BAD_REQUEST)
       if models.haveFunUser.objects.filter(phone__exact=phone):
           return JSONResponse({'desc':'手机号码已存在'},status=HTTP_400_BAD_REQUEST)
       serializer = serializers.UserSerializer(data=data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           dic['result'] = serializer.data
           dic['desc']='注册成功'
           return JSONResponse(dic,status=HTTP_200_OK)
       return JSONResponse({'desc':serializer.errors}, status=HTTP_400_BAD_REQUEST)
       


class ArticalTagViewSet(viewsets.ModelViewSet):
   queryset = models.ArticalTag.objects.all()
   serializer_class = serializers.ArticalTagSerializer
   # permission_classes = (IsOwnerOrReadOnly)
   # def perform_create(self, serializer):
   #     print(self.request.user)
   #     serializer.save(owner=models.haveFunUser.objects.get(id=self.request.session.get('user_id')))

class ArticalViewSet(viewsets.ModelViewSet):
   queryset = models.Artical.objects.all()
   serializer_class = serializers.ArticalSerializer
   # permission_classes = (IsOwnerOrReadOnly)

   # def perform_create(self, serializer):
   #     print(self.request.user)
   #     serializer.save(owner=models.haveFunUser.objects.get(id=self.request.session.get('user_id')))

class UserViewSet(viewsets.ModelViewSet):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserInforSerializer

#用于保存文章草稿
@csrf_exempt
def artical_draft_save(request):
    if request.method == 'POST':
        title =request.POST.get('title')
        content = request.POST.get('content')
        user_id = request.session['user_id']
        tag_id = request.POST.get('tag_id')
        if not user_id:
            return HttpResponse("请先登录")
        if not title:
            return HttpResponse("请先填写文章标题")
        user = models.haveFunUser.objects.filter(user_id__exact=user_id)
        if not user:
            return HttpResponse("请先登录")
        dic = {'title':title,'content':content,'tag_id':tag_id,'owner_id':user_id}
        models.ArticalDraft.objects.create(**dic)
    
    return HttpResponse("保存成功")


#用于获取用户文集
class UserArticalTagAPIView(APIView):
   queryset = models.ArticalTag.objects.all()
   serializer_class = serializers.ArticalTagSerializer
   permission_classes = (permissions.IsAuthenticated,)   
   def post(self, request, format=None):
       user_id = request.session['user_id'];
       if int(user_id)>0:
           tag = models.ArticalTag.objects.filter(createdByUser_id__exact=user_id)
           data=serializers.ArticalTagSerializer(tag,many=True)
           dic = {'result':data.data,'desc':'获取成功'}
           return JSONResponse(dic, status=HTTP_200_OK)
       return JSONResponse({'desc':'请先登录'}, status=HTTP_400_BAD_REQUEST)
 

# 用户获取文章列表
@csrf_exempt
def Artical_list_api(request):
  if request.method == 'POST':
    arr = models.Artical.objects.all().order_by('article_id') #order_by必须有 不然分页失败
    return api_paging(arr, request, serializers.ArticalSerializer) #分页处理
    

# 用户获取文集列表
@csrf_exempt
def Artical_Tag_List_api(request):
  if request.method == 'POST':
    arr = models.ArticalTag.objects.all().order_by('tag_id')
    data=serializers.ArticalTagSerializer(arr,many=True)
    dic = {'result':data.data,'desc':'获取成功'}
    return JSONResponse(dic, status=HTTP_200_OK)

class UserChnageAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserInforSerializer
   permission_classes = (permissions.AllowAny,)
# 修改用户信息
   def post(self, request, format=None):
      print('xxxxxchange_user_info')
      if request.method == 'POST':	
          user_id = request.POST.get('user_id')
          sex =request.POST.get('sex')
          email = request.POST.get('email')
          address = request.POST.get('address')
          user = models.haveFunUser.objects.filter(user_id__exact=user_id)
          print('change_user_info======')
          if user:
              if sex:
                user.update(sex=sex)
              if email:
                user.update(email=email)
              if address:
                user.update(address=address)
              user = user.first()
              serializer = serializers.UserInforSerializer(user)
              return JSONResponse({'result':serializer.data,'desc':'修改成功'}, status=HTTP_200_OK)
          else:
            return JSONResponse( {'desc':'没有此用户'},status=HTTP_400_BAD_REQUEST)

#上传文章
@csrf_exempt
def Artical_upload_api(request):
  if request.method == 'POST':
      title =request.POST.get('title')
      content = request.POST.get('content')
      user_id = request.POST.get('user_id')
      tag_id = request.POST.get('tag_id')
      if not user_id:
          return JSONResponse( {'desc':'请先登录'},status=HTTP_400_BAD_REQUEST)
      if not title:
          return JSONResponse( {'desc':'请先填写文章标题'},status=HTTP_400_BAD_REQUEST)
      if not tag_id:
          return JSONResponse( {'desc':'请选择文集'},status=HTTP_400_BAD_REQUEST)
      dic = {'title':title,'content':content,'tag_id':tag_id,'owner_id':user_id}
      models.Artical.objects.create(**dic)
      return JSONResponse({'desc':'保存成功'}, status=HTTP_200_OK)         
#APP获取用户文集
@csrf_exempt
def tag_list_api(request):
  if request.method == 'POST':  
       user_id = request.POST.get('user_id')
       if user_id:
           tag = models.ArticalTag.objects.filter(createdByUser_id__exact=user_id)
           data=serializers.ArticalTagSerializer(tag,many=True)
           dic = {'result':data.data,'desc':'获取成功'}
           return JSONResponse(dic, status=HTTP_200_OK)
       return JSONResponse({'desc':'请先登录'}, status=HTTP_400_BAD_REQUEST)
