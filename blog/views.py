from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
# from . import models
from .models import *
from django.core import serializers
try:
    import simplejson as json
except:
    import json

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt


def get_model_fields(model):
    json_str = serializers.serialize('json', [model, ], use_natural_foreign_keys=True)
    model_list = json.loads(json_str)
    if len(model_list) > 0:
        data = model_list.pop(0)
        data['fields']['uuid'] = data['pk']
        return data['fields']
    else:
        return None


def get_models_fields(models):
    res_data = []
    if not models or len(models) == 0:
        return res_data
    json_str = serializers.serialize('json', models, use_natural_foreign_keys=True)
    model_list = json.loads(json_str)
    for model in model_list:
        model['fields']['uuid'] = model['pk']
        res_data.append(model['fields'])

    return res_data


def get_create_model_fields(obj):
    data = obj.__dict__
    del data['_state']
    return data


# chenming  chenming@upvi.com cm19900408  超级用户
def index(request):
    # artical = Artical.objects.get()
    artical = Artical.objects.all();
    return render(request, 'index.html', {'result': artical})


def detail(request, page_id):
    detail = Artical.objects.get(pk=page_id)
    return render(request,'detail.html',{'detail': detail})


def edit(request, page_id):
    if str(page_id) == '0':
        return render(request, 'edte.html')
    artice = Artical.objects.get(pk=page_id)
    return render(request, 'edte.html',{'detail': artice})


def edit_action(request):
    title = request.POST.get('title', '默认值')
    content = request.POST.get('content', '默认值')
    page_id = request.POST.get('page_id', '0')
    if page_id == '0':
        Artical.objects.create(title=title, content=content)
        artical = Artical.objects.all();
        return render(request, 'index.html', {'result': artical})

    artical = Artical.objects.get(pk=page_id)
    artical.title = title
    artical.content = content
    artical.save()
    return render(request, 'detail.html', {'detail': artical})


'''
完全纯数据结构
'''


def example(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    word = request.GET.get('word', '')
    time = request.GET.get('time', 'down')
    hot = request.GET.get('hot', 'down')
    classify = request.GET.get('classifiy', '')
    if classify == 'recommend':
        classify = ''
    if time == 'down':
        time = '-updated_at'
    else:
        time = 'updated_at'

    if hot == 'down':
        hot = 'hots'
    else:
        hot = '-hots'
    # order_by 用于排序， -代表倒序排列
    # 现过滤查询在分页
    artical = Artical.objects.filter(title__contains=word, classify__contains=classify).order_by(hot).order_by(time)
    pagedata = Paginator(artical, page_size)
    if pagedata.num_pages < int(page):
        return JsonResponse({'total': 0, 'items': []})
    p1 = pagedata.page(page)

    p2 = []
    for x in p1:
        dicts = x.to_dict()
        for n in dicts:
            if n == 'user':
                del dicts[n]['password']
                del dicts[n]['phone']
                del dicts[n]['prefix']
                del dicts[n]['agree']
                del dicts[n]['created_at']
                del dicts[n]['updated_at']
        p2.append(dicts)
    response = JsonResponse({'total': pagedata.count, 'items': p2})
    return response


def delexam(request, del_id):
    if request.method == 'DELETE':
        Artical.objects.filter(pk=del_id).delete()
        return JsonResponse({})


def postexam(request):
    try:
        result = json.loads(request.body)
        if len(result['title']) > 102:
            return JsonResponse({'code': 400, 'msg': '标题长度超出要求，请减少长度'})
        Artical.objects.create(**result)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'code': 400, 'err': str(e)})


def putexam(request, put_id):
    result = json.loads(request.body)
    if request.method == 'PUT':
        artical = Artical.objects.get(pk=put_id)
        artical.title = result['title']
        artical.content = result['content']
        artical.classify = result['classify']
        artical.save()
        return JsonResponse({})
    else:
        return JsonResponse({'code': 400, 'msg': '方法错误！'})


def details(request, page_id):
    detail_message = Artical.objects.get(id=page_id)
    detail_message.hots += 1
    detail_message.save()
    dicts = detail_message.to_dict()
    for n in dicts:
        if n == 'user':
            del dicts[n]['password']
            del dicts[n]['phone']
            del dicts[n]['prefix']
            del dicts[n]['agree']
            del dicts[n]['created_at']
            del dicts[n]['updated_at']
    return JsonResponse(dicts)


# 用户下的文章列表
def artical_user(request, user_id):
    artical = Artical.objects.filter(user_id=user_id)
    p2 = []
    for x in artical:
        dicts = x.to_dict()
        for n in dicts:
            if n == 'user':
                dicts[n] = {}
        p2.append(dicts)
    return JsonResponse({'total': len(p2), 'items': p2})


# 用户信息
def user_list(request):
    users = User.objects.all()
    response = JsonResponse({'items': get_models_fields(users)})
    return response


# 创建用户
def create_user(request):
    result = json.loads(request.body)
    User.objects.create(**result)
    return JsonResponse({})


# 编辑用户
def edit_user(request, user_id):
    result = json.loads(request.body)
    user_detail = User.objects.get(pk=user_id)
    user_detail.nickname = result['nickname']
    user_detail.web_site = result['web_site']
    user_detail.avatar = result['avatar']
    user_detail.save()
    return JsonResponse({})


# 登录
def login(request):
    users = User.objects.all()
    result = json.loads(request.body)
    for x in users:
        if x.user_name == result['username'] and x.password == result['password']:
            return JsonResponse(get_create_model_fields(x))
    return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})


# 获取用户详情
def get_user(request, user_id):
    user_detail = User.objects.get(pk=user_id)
    dicts = user_detail.to_dict()
    new_dict = {}
    for n in dicts:
        if n == 'password' or n == 'agree':
            pass
        else:
            if n == 'avatar':
                dicts['avatar'] = str(dicts['avatar'])
                new_dict[n] = str(dicts[n])
            new_dict[n] = str(dicts[n])
    return JsonResponse(new_dict)


# 上传头像
def upload_avatar(request, user_id):
    user_detail = User.objects.get(pk=user_id)
    file_content = ContentFile(request.FILES['avatar'].read())
    user_detail.avatar.save(request.FILES['avatar'].name, file_content)
    return JsonResponse({"path": user_detail.avatar.name})


# 评论列表
def comment_list(request):
    ar_id = request.GET.get('artical_id', '')

    arse = Artical.objects.filter(id=ar_id).first()
    if arse:
        comments = arse.artical_comment.all()
    else:
        comments = []
    p1 = list()
    for x in comments:
        dicts = x.to_dict()
        p1.append(dicts)
    return JsonResponse({'items': p1})


# 创建评论
def post_comment(request):
    try:
        result = json.loads(request.body)
        artical_obj = Artical.objects.get(id=result['belong_artical'])
        user_obj = User.objects.get(id=result['belong_user'])
        new_obj = dict()
        new_obj['word'] = result['word']
        new_obj['belong_artical'] = artical_obj
        new_obj['belong_user'] = user_obj
        Comment.objects.create(**new_obj)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': str(e)})