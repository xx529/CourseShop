# Generated by Django 2.1.8 on 2020-03-13 15:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseType', models.CharField(max_length=50, unique=True, verbose_name='课程种类')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=60, verbose_name='课程名称')),
                ('fileName', models.FileField(upload_to='', verbose_name='文件名称')),
                ('imgName', models.ImageField(upload_to='', verbose_name='图片名称')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='价格')),
                ('summary', models.CharField(default='', max_length=1000, verbose_name='课程介绍')),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='是否收费')),
                ('createDatetime', models.DateTimeField(default=datetime.datetime(2020, 3, 13, 23, 56, 21, 246687), verbose_name='创建时间')),
                ('pCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_set', to='course.Category', verbose_name='种类')),
                ('userBuyer', models.ManyToManyField(related_name='userBuyer_set', to='user.User', verbose_name='购买用户')),
                ('userShopcar', models.ManyToManyField(related_name='userShopcar_set', to='user.User', verbose_name='加入购物车用户')),
            ],
        ),
    ]