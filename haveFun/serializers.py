# quickstart/serializers.py
from django.contrib.auth.models import *
from rest_framework import serializers
from . import models
import time
from django.conf import settings




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.userHeadImage
        fields = ('image_id','image')


#用户基本信息
class UserSerializer(serializers.ModelSerializer):
    time_join = serializers.SerializerMethodField()
    def get_time_join(self,obj):
        t = obj.date_joined
        return t.strftime('%Y-%m-%d %X')
    class Meta:
        model = models.haveFunUser
        fields = ('user_id','name', 'phone','time_join','sex','age','address','email','img','user_type','passwd')

#查询用户全部信息
class UserInforSerializer(serializers.ModelSerializer):
    # artical_set = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Artical.objects.all())
    # articalTag_set = serializers.PrimaryKeyRelatedField(many=True, queryset=models.ArticalTag.objects.all())
    article_count = serializers.SerializerMethodField()
    artical_tag_count = serializers.SerializerMethodField()
    time_join = serializers.SerializerMethodField()
    class Meta:
        model = models.haveFunUser
        fields = ('user_id','name', 'phone','time_join','sex','age','address','email','img','user_type','article_count','artical_tag_count')
    def get_article_count(self, obj):
        return models.Artical.objects.filter(owner_id__exact=obj.user_id).count()
    def get_artical_tag_count(self, obj):
        return models.ArticalTag.objects.filter(createdByUser_id__exact=obj.user_id).count()
    def get_time_join(self,obj):
        t = obj.date_joined
        return t.strftime('%Y-%m-%d %X')

class ArticalTagSerializer(serializers.ModelSerializer):
    createdByUser = UserInforSerializer(many=False)
    create_Time = serializers.SerializerMethodField()
    def get_create_Time(self,obj):
        t = obj.createTime
        return t.strftime('%Y-%m-%d %X')
    class Meta:
        model = models.ArticalTag
        fields = ('tag_id','tag_name','createdByUser','create_Time','tag_abstract','tag_img')

class ArticalSerializer(serializers.ModelSerializer):
    owner = UserInforSerializer(many=False) 
    # tag = serializers.ReadOnlyField(source='tag.tag_name') #只读
    tag = ArticalTagSerializer(many=False)
    pubTime = serializers.SerializerMethodField()
    def get_pubTime(self,obj):
        t = obj.pub_time
        return t.strftime('%Y-%m-%d %X')
    class Meta:
        model = models.Artical
        fields = ('article_id','title', 'content', 'pubTime', 'tag','read','collect','command','owner','image')



