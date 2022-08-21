from django.contrib import admin
from .models import Course,Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['courseType']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseName','pCategory','status','price','imgName','fileName']
    filter_horizontal = ['userBuyer','userShopcar']