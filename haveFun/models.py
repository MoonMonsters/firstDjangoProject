#encoding:utf-8
from django.db import models
import json
import time



class haveFunUser(models.Model):
    user_id = models.AutoField(primary_key=True,default=1)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11,unique=True)
    date_joined = models.DateTimeField(auto_now=True)  #DateField
    gender_choices = ((0,"男"),(1,"女"))
    sex = models.IntegerField(choices=gender_choices,default=1)
    age = models.PositiveIntegerField(default=18)
    address = models.CharField(max_length=80,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    img = models.TextField(null=True,blank=True)
    user_type_choice=((0,"超级用户"),(1,"普通用户"))
    user_type = models.IntegerField(choices=user_type_choice,default=1)
    passwd = models.CharField(max_length=64)
    def __str__(self):
        return self.name,self.phone


class userHeadImage(models.Model):
    image_id = models.AutoField(primary_key=True,default=1)
    image = models.ImageField(max_length=None,upload_to='head_images')
    uploaded_by = models.IntegerField(unique=True)

class articalHeadImage(models.Model):
    image_id = models.AutoField(primary_key=True,default=1)
    image = models.ImageField(max_length=None,upload_to='artical_image')
    uploaded_by = models.IntegerField(unique=False)
    filename = models.CharField(max_length=100,default = '')
    
class ArticalTagImage(models.Model):
    image_id = models.AutoField(primary_key=True,default=1)
    image = models.ImageField(max_length=None,upload_to='ArticalTag')
    uploaded_by = models.IntegerField(unique=True)
    filename = models.CharField(max_length=100,default = '')
    
class ArticalTag(models.Model):
    tag_id = models.AutoField(primary_key = True,default=1)
    tag_name = models.CharField(max_length=64)
    tag_abstract = models.CharField(max_length=128,default='')
    createdByUser = models.ForeignKey("haveFunUser")
    createTime = models.DateTimeField(auto_now_add=True)
    tag_img = models.TextField(null=True,blank=True)
    def __str__(self):
        return tag_name
    class Meta:
        ordering = ['createTime']
        unique_together = (('tag_id','tag_name','createdByUser','createTime','tag_abstract','tag_img'),)
  
class ArticalManager(models.Manager):
    def create(self, *args, **kwargs):
        # kwargs['content'] = '---------'
        # kwargs['pub_time'] = time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        print('manager-artcal----create--',kwargs)
        super(ArticalManager, self).create(*args, **kwargs)  
class Artical(models.Model):
    article_id = models.AutoField(primary_key=True,default=1)
    title = models.CharField(max_length=60)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("ArticalTag")
    read = models.PositiveIntegerField(default=0)
    collect = models.PositiveIntegerField(default=0)
    command = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey("haveFunUser")
    image = models.TextField(null=True,blank = True)
    objects = ArticalManager()
    def __str__(self):
        return self.title,self.owner.name
    # def save(self, *args, **kwargs):
    #     print('artical-saving--')
    #     self.pub_time = datetime.datetime.now()
    #     print(kwargs,args)
        # self.read = 0
        # self.collect = 0
        # self.command = 0
        # super(Artical, self).save(*args, **kwargs)

    
class ArticalDraft(models.Model):
    articalDraft_id = models.AutoField(primary_key = True,default=1)
    title = models.CharField(max_length=60)
    content = models.TextField()
    time =  models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("ArticalTag")
    owner = models.ForeignKey("haveFunUser")
    image = models.TextField(null=True,blank = True)
    def __str__(self, arg):
        return title

        
