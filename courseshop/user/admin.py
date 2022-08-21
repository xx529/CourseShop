from django.contrib import admin
from .models import User
# Register your models here.

admin.site.site_header = 'CSDN课程商城后台管理'
admin.site.index_title = '后台系统'
admin.site.site_title = 'CSDN'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','password','money','gender','tel']
    list_filter = ['gender']
    search_fields = ['tel','username']



