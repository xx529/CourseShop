from django.shortcuts import render,HttpResponse
from .models import Course,Category
from user.models import User
from django.http import StreamingHttpResponse
import os
import re

# Create your views here.
def index_handler(request):
    context = request.context
    course_data_s = []
    category_s = Category.objects.all()
    for category in category_s:
        course_data_s.append(
            {
                'category':category.courseType,
                'course_s':category.course_set.all()
            }
        )
    context['course_data_s'] = course_data_s
    return render(request,'index.html',context)

def course_handler(request,course_id):
    context = request.context
    course = Course.objects.get(id=course_id)
    session_user = request.session.get('session_user',None)
    try:
        if session_user:
            context['course_per'] = User.objects.filter(id=session_user.get('id'),userBuyer_set=course_id).exists()
            context['course_add'] = User.objects.filter(id=session_user.get('id'),userShopcar_set=course_id).exists()
        context['course'] = course
        return render(request,'course.html',context)
    except:
        return HttpResponse(status=404)

def video_handler(request,course_id):
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        boolean_buyed = User.objects.filter(id=session_user.get('id'),userBuyer_set__id=course_id).exists()
        if boolean_buyed:
            context['course'] = course
            return render(request,'video.html',context)
        else:
            return redirect(reverse('course_course',args=(course.id)))
    except:
        return HttpResponse(status=404)

def videoStream_handler(request,course_id):
    def read_video(filepath,length,offset):
        with open(filepath,'rb') as f:
            f.seek(offect)
            while True:
                data = f.read(length)
                if data:
                    yield data
                else:
                    break
    context = request.context
    try:
        course = Course.objects.get(id=course_id)
        session_user = request.session['session_user']
        boolean_buyed = User.objects.filter(id=session_user.get('id'), userBuyer_set__id=course_id).exists()
        if boolean_buyed:
            context['course'] = course
            request_range = request.headers.get('range')
            start_bytes = re.findall('=(\d+)-',request_range)
            start_bytes = int(start_bytes[0]) if start_bytes else 0
            last_bytes = start_bytes + 1024 * 1024
            size = os.path.getsize(course.fileName.__str__())
            last_bytes = min (last_bytes,size-1)
            length = last_bytes - start_bytes + 1
            response = StreamingHttpResponse(
                read_video(
                    filepath=course.fileName.__str__(),
                    length=length,
                    offset=start_bytes
                ),
                status=206
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = 'byte %s-%s/%s'%(start_bytes,last_bytes,size)
            return response
        else:
            return redirect(reverse('course_course', args=(course.id)))
    except:
        return HttpResponse(status=404)


