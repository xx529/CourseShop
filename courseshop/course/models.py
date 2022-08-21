from django.db import models
import datetime
from user.models import User
import os

# Create your models here.

def save_file(instance,filename):
    return os.path.join('static','video',filename)

def save_img(instance,filename):
    return os.path.join('static','img',filename)

class Category(models.Model):
    class Meta():
        verbose_name = verbose_name_plural = '课程种类表'
    courseType = models.CharField(max_length=50,unique=True,verbose_name='课程种类')

    def __str__(self):
        return self.courseType

class Course(models.Model):
    STATUS_CHOICES = (
        (0,'免费'),
        (1,'收费')
    )
    class Meta():
        verbose_name = verbose_name_plural = '课程表'

    courseName = models.CharField(max_length=60,verbose_name='课程名称')
    fileName = models.FileField(upload_to=save_file,verbose_name='文件名称')
    imgName = models.ImageField(upload_to=save_img,verbose_name='图片名称')
    pCategory = models.ForeignKey(to=Category,on_delete=models.CASCADE,related_name='course_set',verbose_name='种类')
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='价格',blank=True)
    summary = models.CharField(max_length=1000,default='',verbose_name='课程介绍',blank=True)
    status = models.PositiveSmallIntegerField(default=0,verbose_name='是否收费',blank=True,choices=STATUS_CHOICES) # 0为不收费
    createDatetime = models.DateTimeField(default=datetime.datetime.now(),verbose_name='创建时间',blank=True)
    userBuyer = models.ManyToManyField(to=User,related_name='userBuyer_set',verbose_name='购买用户',blank=True)
    userShopcar = models.ManyToManyField(to=User,related_name='userShopcar_set',verbose_name='加入购物车用户',blank=True)

