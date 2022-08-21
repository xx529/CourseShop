from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index_handler,name='index_handler'),
    re_path('coures/(.+)',views.course_handler,name='course_course'),
    re_path('video/(.+)',views.video_handler,name='course_video'),
    re_path('videoStream/(.+)',views.videoStream_handler,name='course_videoStream'),
]