#encoding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from . import models
from django.http import JsonResponse

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    articals = models.Artical.objects.all()
    return render(request,'haveFun/index.html',{'articals':articals})
#作者页面
def author(request,username):
    user = models.haveFunUser.objects.get(name__exact=username)
    articals = models.Artical.objects.filter(owner_id__exact = user.user_id)
    return render(request,'haveFun/author.html',{'author':user,'articals':articals})


def myHome(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return render(request,'haveFun/login.html')
    user = models.haveFunUser.objects.filter(user_id__exact=user_id)
    return render(request,'haveFun/mine.html',{'mine':user})

def tagList(request):
    tagLists = models.ArticalTag.objects.all()
    return render(request,'haveFun/tagList.html',{'tagList':tagLists})

def tag_detail(request,tag_id):
    tag = models.ArticalTag.objects.get(tag_id__exact = tag_id)
    articals = models.Artical.objects.filter(tag__exact = tag_id)
    return render(request,'haveFun/tag_detail.html',{'tagdetail':tag,'articals':articals})



# 发表文章界面
def pup_page(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return render(request,'haveFun/login.html')
    return render(request,'haveFun/write.html',{'user_id':user_id,})


#获取用户文集

def get_userTag(request):
    user_id = request.session.get("user_id")
    tag = models.ArticalTag.objects.filter(createdByUser_id = user_id)
    lists = serializers.serialize('json', tag,fields = ('tag_id','tag_name','createdByUser','createTime','tag_abstract','tag_img'))
    result={}
    result['result']=lists
    print(json.dumps(result))
    return HttpResponse(json.dumps(result,cls=serializers.json.DjangoJSONEncoder), content_type='application/json')

#根据文集获取文章列表
def get_articalBy_tag(request,tag_id):
    artical = models.Artical.objects.filter(tag_id__exact = tag_id)
    lists = serializers.serialize('json', artical)
    result={}
    result['result']=lists
    print(json.dumps(result))
    return HttpResponse(json.dumps(result,cls=serializers.json.DjangoJSONEncoder), content_type='application/json')



#文章详情
def artical_detail(request,artical_id):
    artical = models.Artical.objects.get(article_id__exact = artical_id)
    print('-------------',request.method)
    if request.method == 'POST':
        lists =[]
        lists.append( artical)
        result={}
        result['result']=serializers.serialize('json', lists)
        print(json.dumps(result))
        return HttpResponse(json.dumps(result,cls=serializers.json.DjangoJSONEncoder), content_type='application/json')
    return render(request,'haveFun/artical_detail.html',{'artical':artical})

#web登录事件
def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('passwd')
        request.session['username'] = username
        if not models.haveFunUser.objects.filter(name__exact=username):
            print('用户不存在')
            return render(request, 'haveFun/login.html', {'error': '用户不存在'})
        user = models.haveFunUser.objects.get(name__exact=username)
        if  user.passwd == password:
       # 记忆已登录用户
            request.session['user_id'] = user.user_id
            articals = models.Artical.objects.all()
            print(user.name)
            return render(request,'haveFun/index.html',{'articals':articals})
        print("密码错误")
        return render(request, 'haveFun/login.html', {'error': "密码错误"})
    return render(request,'haveFun/login.html')

def register(request):
	return render(request,'haveFun/register.html')

def edit_page(request,article_id):
	if article_id:
		if models.Artical.objects.filter(article_id__exact=article_id):
		    return render(request,'haveFun/write.html',{'artical':artical})
		else:render(request,'haveFun/write.html')
	else:
	    return render(request,'haveFun/write.html')


# 仿美团首页界面
def meiHome(request):
    return render(request,'haveFun/sy.html')

# 仿美团附近页面
def meiNeibor(request):
    return render(request,'haveFun/fujin.html')