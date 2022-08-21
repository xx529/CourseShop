from django.shortcuts import render,HttpResponse,redirect,reverse
from user.models import User
from course import views as course_views
from course.models import Course

# Create your views here.
def index_handler(request):
    context = request.context
    session_user = request.session['session_user']
    user = User.objects.get(id=session_user['id'])
    context['user'] = user
    if request.method == 'GET':
        return render(request,'user.html',context)
    else:
        user.username = request.POST.get('username')
        user.gender = request.POST.get('gender')
        user.tel = request.POST.get('tel')
        user.save()
        return redirect(reverse('user_index'))

def course_handler(request):
    context = request.context
    user = User.objects.get(id=request.session['session_user'].get('id'))
    course_s = user.userBuyer_set.all()
    context['course_s'] = course_s
    return render(request,'user_course.html',context)

def login_handler(request):
    if request.method != 'POST':
        return HttpResponse(statue=403)
    context = request.context
    account = request.POST.get('account')
    password = request.POST.get('password')
    user_s = User.objects.filter(account=account,password=password)
    if user_s:
        user = user_s[0]
        request.session['session_user'] = {'id':user.id,'account':user.account}
        context['session_user'] = {'id':user.id,'account':user.account}
        return redirect(reverse('index_handler'))
    else:
        context['login_message'] = '用户名不存在或者密码错误'
        return course_views.index_handler(request)

def register_handler(request):
    if request.method != 'POST':
        return HttpResponse(status=403)
    context = request.context
    account = request.POST.get('account')
    password = request.POST.get('password')
    user_exists = User.objects.filter(account=account).exists()
    try:
        if not user_exists:
            user = User(account=account,password=password)
            user.save()
            request.session['session_user'] = {'id':user.id,'account':user.account}
        else:
            context['register_message'] = '账号已经存在'
    except:
        context['register_message'] = '服务器异常'
    finally:
        return course_views.index_handler(request)

def logout_handler(request):
    request.session['session_user'] = None
    return redirect(reverse('index_handler'))

def purchase_handler(request,id):
    context = request.context
    course = Course.objects.get(id=id)
    user = User.objects.get(id=request.session['session_user'].get('id'))
    try:
        if user.money < course.price:
            context['message'] = '余额不足'
        else:
            user.money = user.money - course.price
            user.userBuyer_set.add(course)
            boolean_add = User.objects.filter(id=request.session['session_user'].get('id'),userShopcar_set__id=course.id).exists()
            if boolean_add:
                user.userShopcar_set.remove(course)
            user.save()
            context['message'] = '购买成功'
    except:
        context['message'] = '购买失败'
    finally:
        return render(request,'user_message.html',context)

def addShoppingCar_handler(request,id):
    context = request.context
    try:
        course = Course.objects.get(id=id)
        user = User.objects.get(id=request.session['session_user'].get('id'))
        user.userShopcar_set.add(course)
        user.save()
        course_s = user.userShopcar_set.all()
        context['course_s'] = course_s
        context['message'] = '加入购物车成功'
    except:
        context['message'] = '加入购物车失败'
    return render(request,'user_message.html',context)

def shoppingCar_handler(request):
    context = request.context
    user = User.objects.get(id=request.session['session_user'].get('id'))
    course_s = user.userShopcar_set.all()
    context['course_s'] = course_s
    return render(request, 'user_shoppingcart.html', context)