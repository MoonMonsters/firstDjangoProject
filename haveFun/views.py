
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
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from haveFun.permissions import IsOwnerOrReadOnly

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


        
        
    

def api_paging(objs, request, Ser):
    """
    objs : 实体对象
    request : 请求对象
    Serializer : 对应实体对象的序列化
    """
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
    }, status=HTTP_200_OK) #返回
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
   serializer_class = serializers.UserLoginSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       password = data.get('passwd')
       if not models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':'用户名不存在'},status=HTTP_400_BAD_REQUEST,)
       user = models.haveFunUser.objects.get(name__exact=username)
       if user.passwd == password:
           serializer = serializers.UserSerializer(user)
           new_data = serializer.data
           print(new_data)
           # 记忆已登录用户
           self.request.session['user_id'] = user.user_id
           self.request.session['user_name'] = user.name
           return JSONResponse({'result':serializer.data,'desc':'登陆成功'}, status=HTTP_200_OK)
       dic['desc'] = 'password error'
       return JSONResponse( dic,status=HTTP_400_BAD_REQUEST)

#用于注册

class UserRegisterAPIView(APIView):
   queryset = models.haveFunUser.objects.all()
   serializer_class = serializers.UserRegisterSerializer
   permission_classes = (permissions.AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('name')
       dic = {}
       if models.haveFunUser.objects.filter(name__exact=username):
           return JSONResponse({'desc':用户名已存在},status=HTTP_400_BAD_REQUEST)
       serializer = serializers.UserRegisterSerializer(data=data)
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
   serializer_class = serializers.UserSerializer

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

    # except:
      # dic = {'message':'no more data','result':[]}
      # return JSONResponse(dic,status=HTTP_200_OK)
    

# 用户获取文集列表
@csrf_exempt
def Artical_Tag_List_api(request):
  if request.method == 'POST':
    arr = models.ArticalTag.objects.all().order_by('tag_id')
    data=serializers.ArticalTagSerializer(arr,many=True)
    dic = {'result':data.data,'desc':'获取成功'}
    return JSONResponse(dic, status=HTTP_200_OK)
	