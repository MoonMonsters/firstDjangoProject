# quickstart/serializers.py
from django.contrib.auth.models import *
from rest_framework import serializers
from . import models
import time
from django.conf import settings



class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)#use_url=True是否显示完整的路径
    def create(self, validated_data):
        data = self.context.get('request').data.dict()
        user_id = data['user_id']       
        print('xxxx=------',user_id,'xasaaaaa=---',validated_data)
        validated_data.update({'uploaded_by': user_id})
        return models.userHeadImage.objects.create(**validated_data)
    class Meta:
        model = models.userHeadImage
        fields = ('image_id','image')

class ArticalImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)#use_url=True是否显示完整的路径
    def create(self, validated_data):
        print('upload--artical-photo--')
        data = self.context.get('request').data.dict()
        user_id = data['uploaded_by']       
        print('user_id=------',validated_data)
        validated_data.update({'uploaded_by': user_id})
        validated_data.update({'filename': data['filename']})
        return models.articalHeadImage.objects.create(**validated_data)
    class Meta:
        model = models.articalHeadImage
        fields = ('filename','image','uploaded_by')


#用户基本信息
class UserSerializer(serializers.ModelSerializer):
    time_join = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    def get_time_join(self,obj):
        t = obj.date_joined
        return t.strftime('%Y-%m-%d %X')
    def get_img(self,obj):
        if not models.userHeadImage.objects.filter(uploaded_by__exact=obj.user_id):
            return ''
        image = ImageSerializer(models.userHeadImage.objects.filter(uploaded_by__exact=obj.user_id).first()).data
        if image:
            return image['image']
        else:
            return ''
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
    img = serializers.SerializerMethodField()
    def get_img(self,obj):
        image = ImageSerializer(models.userHeadImage.objects.filter(uploaded_by__exact=obj.user_id).first()).data
        print(image)
        if image:
            return image['image']
        else:
            return ''
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
    article_count = serializers.SerializerMethodField()
    def get_create_Time(self,obj):
        t = obj.createTime
        return t.strftime('%Y-%m-%d %X')
    def get_article_count(self, obj):
        return models.Artical.objects.filter(tag_id__exact=obj.tag_id).count()
    class Meta:
        model = models.ArticalTag
        fields = ('tag_id','tag_name','createdByUser','create_Time','tag_abstract','tag_img','article_count')

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



