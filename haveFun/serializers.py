# quickstart/serializers.py
from django.contrib.auth.models import *
from rest_framework import serializers
from . import models


class MyCustField(serializers.CharField):
    """为 Model 中的自定义域额外写的自定义 Serializer Field"""

    def to_representation(self, obj):
        """将从 Model 取出的数据 parse 给 Api"""
        return obj

    def to_internal_value(self, data):
        """将客户端传来的 json 数据 parse 给 Model"""
        return json.loads(data.enhelpcode('utf-8'))



#查询用户的基本信息
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.haveFunUser
        fields = ('user_id','name', 'phone','date_joined','sex','age','address','email','img','user_type')
#查询用户全部信息
class UserInforSerializer(serializers.ModelSerializer):
    artical_set = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Artical.objects.all())
    articalTag_set = serializers.PrimaryKeyRelatedField(many=True, queryset=models.ArticalTag.objects.all())
    class Meta:
        model = models.haveFunUser
        fields = ('user_id','name', 'phone','date_joined','sex','age','address','email','img','user_type','artical_set','articalTag_set')
    # 这句话的作用是为 MyModel 中的外键建立超链接，依赖于 urls 中的 name 参数
    # 不想要这个功能的话完全可以注释掉
    # artical_set = serializers.HyperlinkedRelatedField(
    #     many=True, queryset=models.Artical.objects.all(),
    #     view_name='user_artical_list'
    # )
    # articalTag_set = serializers.HyperlinkedRelatedField(
    #     many=True, queryset=odels.ArticalTag.objects.all(),
    #     view_name='user_artical_tag_list'
    # )


class ArticalTagSerializer(serializers.ModelSerializer):
	createdByUser = UserSerializer(many=False) 
	class Meta:
		model = models.ArticalTag
		fields = ('tag_id','tag_name','createdByUser','createTime','tag_abstract','tag_img')

class ArticalSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False) #只读
    # tag = serializers.ReadOnlyField(source='tag.tag_name') #只读
    tag = ArticalTagSerializer(many=False)
    class Meta:
        model = models.Artical
        fields = ('article_id','title', 'content', 'pub_time', 'tag','read','collect','command','owner','image')
    # def create(self, validated_data):
    #   """响应 POST 请求"""
    #   # 自动为用户提交的 model 添加 owner
    #     validated_data['owner'] = self.context['request'].user_id
    #     return models.Artical.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #   """响应 PUT 请求"""
    #     instance.field = validated_data.get('field', instance.field)
    #     instance.save()
    #     return instance


#用于注册时返回的json数据
class UserRegisterSerializer(serializers.ModelSerializer):
   class Meta:
       model = models.haveFunUser
       fields = ('user_id','name', 'phone','date_joined','sex','age','address','email','img','user_type','passwd')
#用于登录返回的json数据
class UserLoginSerializer(serializers.ModelSerializer):
   class Meta:
       model = models.haveFunUser
       fields = ('name','passwd')
