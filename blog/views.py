from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
# from django.core.files.base import ContentFile
import datetime
import time
import os
from django.conf import settings
from django.contrib import auth
# 获取model 以及序列化querySet
from .models import *
from django.core import serializers

# 获取post请求的参数
try:
    import simplejson as json
except:
    import json

from rest_framework.decorators import api_view
from .serializers import ArticalSerializer, PageNumberPagination
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET', 'POST'])
@csrf_exempt
def artical_list(request):
    if request.method == 'GET':
        query = request.query_params
        if query['group'] == 'time':
            time_check = query['time']
            if time_check == 'down':
                time_check = '-created_at'
            else:
                time_check = 'created_at'
            articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(time_check)

        elif query['group'] == 'hot':
            hot = query['hot']
            if hot == 'down':
                hot = 'hots'
            else:
                hot = '-hots'
            articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(hot)

        elif query['group'] == 'nice':
            nice = query['nice']
            if nice == 'down':
                nice = 'nices'
            else:
                nice = '-nices'
            articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(nice)
        else:
            pass

        page_obj = PageNumberPagination()
        page_data = page_obj.paginate_queryset(articals, request)
        ser_obj = ArticalSerializer(page_data, many=True)
        return page_obj.get_paginated_response(ser_obj.data)

    elif request.method == 'POST':
        serializer = ArticalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response({}, status=200)
        return Response(serializer.errors, status=500)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def artical_detail(request, pk):
    try:
        artical = Artical.objects.get(pk=pk)
    except Artical.DoseNotExist:
        return Response(status=404)

    if request.method == 'GET':
        req = {"hots": artical.hots + 1}
        serializer = ArticalSerializer(artical, data=req)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=500)

    elif request.method == 'PUT':
        serializer = ArticalSerializer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        artical.delete()
        return Response({}, status=200)


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
完全纯数据结构, 前后端分离开始处----------------------------------
'''


# 验证
def verifi(func):
    def inner(request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            id = token[4:36]
            old_time = float(token[37:])
            # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(old_time))
            # print(otherStyleTime)
            has_id = User.objects.get(id=id)
            if has_id:
                now_time = time.time()
                if (now_time - old_time) / 60 > 30:
                    return HttpResponse('用户登录失效', status=401)
            else:
                return HttpResponse('用户不存在', status=401)
            return func(request)
        else:
            return HttpResponse('Unauthorized', status=401)


    return inner


# 获取查询文章列表
def example(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    group = request.GET.get('group', '')
    word = request.GET.get('word', '')
    classify = request.GET.get('classify', '')
    if classify == 'recommend':
        classify = ''

    # order_by 用于排序， -代表倒序排列
    # 现过滤查询在分页
    if group == 'time':
        time = request.GET.get('time', 'down')
        if time == 'down':
            time = '-created_at'
        else:
            time = 'created_at'
        artical = Artical.objects.filter(title__contains=word, classify__contains=classify).order_by(time)

    elif group == 'hot':
        hot = request.GET.get('hot', 'down')
        if hot == 'down':
            hot = 'hots'
        else:
            hot = '-hots'
        artical = Artical.objects.filter(title__contains=word, classify__contains=classify).order_by(hot)

    elif group == 'nice':
        nice = request.GET.get('nice', 'down')
        if nice == 'down':
            nice = 'nices'
        else:
            nice = '-nices'
        artical = Artical.objects.filter(title__contains=word, classify__contains=classify).order_by(nice)
    else:
        pass

    pagedata = Paginator(artical, page_size)
    if pagedata.num_pages < int(page):
        return JsonResponse({'total': pagedata.count, 'items': []})
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
            if n == 'user_like':
                for k in dicts[n]:
                    del k['password']
                    del k['phone']
                    del k['prefix']
                    del k['agree']
                    del k['created_at']
                    del k['updated_at']
        p2.append(dicts)
    response = JsonResponse({'total': pagedata.count, 'items': p2})
    return response


# 删除其中一个文章
def delexam(request, del_id):
    if request.method == 'DELETE':
        Artical.objects.filter(pk=del_id).delete()
        return JsonResponse({})


# 创建一篇文章
def postexam(request):
    try:
        result = json.loads(request.body)
        if len(result['title']) > 102:
            return JsonResponse({'code': 400, 'msg': '标题长度超出要求，请减少长度'})
        Artical.objects.create(**result)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'code': 400, 'err': str(e)})


# 更新文章
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


# 文章的详情
def details(request, page_id):
    login_user = request.GET.get('login_id', '')
    detail_message = Artical.objects.get(id=page_id)
    detail_message.hots += 1
    detail_message.save()
    dicts = detail_message.to_dict()

    dicts['followed'] = False
    has = FriendShip.objects.filter(followed=detail_message.user.id, follower=login_user).first()
    if has:
        dicts['followed'] = True
    for n in dicts:
        if n == 'user':
            del dicts[n]['password']
            del dicts[n]['phone']
            del dicts[n]['prefix']
            del dicts[n]['agree']
            del dicts[n]['created_at']
            del dicts[n]['updated_at']
        if n == 'user_like':
            for x in dicts[n]:
                del x['password']
                del x['phone']
                del x['prefix']
                del x['agree']
                del x['created_at']
                del x['updated_at']
    return JsonResponse(dicts)


# 某一用户下的文章列表
def artical_user(request, user_id):
    artical = Artical.objects.filter(user_id=user_id)
    p2 = []
    for x in artical:
        dicts = x.to_dict()
        for n in dicts:
            if n == 'user':
                dicts[n] = {}
        p2.append(dicts)
    return JsonResponse({'count': len(p2), 'items': p2})


# 用户列表
def user_list(request):
    users = User.objects.all()
    response = JsonResponse({'items': get_models_fields(users)})
    return response


# 创建用户
def create_user(request):
    result = json.loads(request.body)
    has = User.objects.filter(user_name=result['user_name']).first();
    if has:
        print('存在')
        return JsonResponse({'code': 400, 'msg': '用户名已经存在'})
    else:
        print('不存在')
        User.objects.create(**result)
        latest_user = User.objects.all().order_by('-created_at')[0];
        return JsonResponse(deal_class_person_message(latest_user))


# 编辑用户
def edit_user(request, user_id):
    result = json.loads(request.body)
    user_detail = User.objects.get(pk=user_id)
    if result['nickname']:
        user_detail.nickname = result['nickname']
    if result['web_site']:
        user_detail.web_site = result['web_site']
    if result['avatar']:
        user_detail.avatar = result['avatar']
    user_detail.save()
    return JsonResponse({})


# 获取用户详情
def get_user(request, user_id):
    user_detail = User.objects.get(pk=user_id)
    new_dict = deal_class_person_message(user_detail)
    return JsonResponse(new_dict)

# 方法---去除用户密码等字段
def deal_class_person_message(cls):
    new_dict = {}
    dicts = cls.to_dict()
    for n in dicts:
        if n == 'password' or n == 'agree':
            pass
        else:
            if n == 'avatar':
                new_dict[n] = str(dicts[n])
            else:
                new_dict[n] = dicts[n]
    return new_dict


# 登录
def login(request):
    result = json.loads(request.body)
    username = result['username']
    password = result['password']
    user = User.objects.filter(user_name=username, password=password).first()
    if user:
        new_dict = deal_class_person_message(user)
        new_dict['token'] = '{}-{}'.format(new_dict['id'], time.time())
        print(new_dict['token'])
        return JsonResponse(new_dict)
    return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})


# 上传头像
def upload_avatar(request):
    f1 = request.FILES.get('avatar')
    path = request.FILES.get('avatar').name
    d = datetime.date.today()
    path1 = os.path.join(settings.BASE_DIR, "media", "avatar", d.strftime('%Y'), d.strftime('%m'), d.strftime('%d'), path)
    text = os.path.join(settings.BASE_DIR, "media", "avatar", d.strftime('%Y'), d.strftime('%m'), d.strftime('%d'))
    path2 = os.path.join("avatar", str(d.year), d.strftime('%m'), d.strftime('%d'), path)
    if not os.path.exists(text):
        os.makedirs(text)
    with open(path1, 'wb') as f:
        for c in f1.chunks():
            f.write(c)
    return JsonResponse({'path': path2})


'''
评论相关接口开始处
'''


# 评论列表
def comment_list(request):
    ar_id = request.GET.get('artical_id', '')
    arse = Artical.objects.filter(id=ar_id).first()
    if arse:
        comments = arse.artical_comment.all()
    else:
        comments = []
    p1 = list()
    p2 = list()
    for x in comments:
        dicts = x.to_dict()
        if dicts['to_comment']:
            p2.append(dicts)
        else:
            dicts['comment_children'] = list()
            p1.append(dicts)

    for a in p2:
        for b in p1:
            if b['id'] == a['to_comment']:
                b['comment_children'].append(a)

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
        if 'to_comment' in result and result['to_comment']:
            new_obj['to_comment'] = result['to_comment']
        Comment.objects.create(**new_obj)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'code': 400, 'msg': str(e)})


# 某一用户参与的评论条数列表---个人界面
def comment_user(request):
    ur_id = request.GET.get('user_id', '')
    urse = User.objects.filter(id=ur_id).first()
    if urse:
        comments = urse.comment_user.all()
    else:
        comments = []
    p1 = list()
    for x in comments:
        user = deal_class_person_message(x.belong_user)
        dicts = x.to_dict()
        dicts['belong_user'] = user
        if dicts['to_comment']:
            select_artical = Comment.objects.filter(id=dicts['to_comment']).first()
            ins = deal_class_person_message(select_artical.belong_user)
            dicts['to_comment_dict'] = ins
        p1.append(dicts)
    return JsonResponse({'count': len(p1), 'items': p1})


# 点赞
def post_nice(request):
    result = json.loads(request.body)
    ar_id = result['artical_id']
    article = Artical.objects.get(pk=ar_id)
    if result['action'] == 'like':
        article.user_like.add(result['user_id'])
        article.nices = article.nices + 1
        article.save();
        return JsonResponse({})
    else:
        article.user_like.remove(result['user_id'])
        article.nices = article.nices - 1
        article.save();
        return JsonResponse({})


# 获取用户点赞的文章列表
def get_nice_person(request, user_id):
    user_detail = User.objects.get(pk=user_id)
    users = user_detail.like_user.all();
    p1 = list()
    for x in users:
        dicts = x.to_dict()
        p1.append(dicts)
    return JsonResponse({"count": len(p1), "items": p1})


# 关注 与 取消关注
def post_follow(request):
    result = json.loads(request.body)
    follower_id = result['follower_id']
    followed_id = result['followed_id']
    have = FriendShip.objects.filter(followed=followed_id, follower=follower_id).first()
    if have:
        FriendShip.objects.filter(followed=followed_id, follower=follower_id).delete()
    else:
        # 发出关注的人
        follower = User.objects.get(pk=follower_id)
        # 被关注的人
        followed = User.objects.get(pk=followed_id)
        new_obj = dict()
        new_obj['follower'] = follower
        new_obj['followed'] = followed
        FriendShip.objects.create(**new_obj)
    return JsonResponse({})


# 获取粉丝
def get_fans(request, user_id):
    user_message = User.objects.get(id=user_id)
    print(user_message)
    fans = user_message.followed.all()
    arr = list()
    for x in fans:
        arr.append(x.to_dict())
    return JsonResponse({"count": len(arr), "items": arr})


# 获取关注的人
def get_followers(request, user_id):
    user_message = User.objects.get(id=user_id)
    followers = user_message.follower.all()
    arr = list()
    for x in followers:
        arr.append(x.to_dict())
    return JsonResponse({"count": len(arr), "items": arr})


# 相关游戏记录
def get_game(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    arr = Game.objects.all().order_by('-kilometer')
    pagedata = Paginator(arr, page_size)
    if pagedata.num_pages < int(page):
        return JsonResponse({'total': 0, 'items': []})
    p1 = pagedata.page(page)
    p2 = list()
    for x in p1:
        dicts = x.to_dict();
        for n in dicts:
            if n == 'user':
                del dicts[n]['password']
                del dicts[n]['phone']
                del dicts[n]['prefix']
                del dicts[n]['agree']
                del dicts[n]['created_at']
                del dicts[n]['updated_at']
        p2.append(dicts)
    return JsonResponse({'total': pagedata.count, "items": p2})


# 创建游戏记录
def post_game(request):
    result = json.loads(request.body)
    user_id = result['user_id']
    try:
        user = User.objects.get(id=user_id)
        has_user = Game.objects.filter(user=user).first()
        if has_user:
            if has_user.kilometer < result["kilometer"]:
                has_user.kilometer = result['kilometer']
                has_user.save()
        else:
            new_obj = dict()
            new_obj['kilometer'] = result['kilometer']
            new_obj['user'] = user
            Game.objects.create(**new_obj)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'code': 400, 'err': str(e)})


# 测试接口
def back_env(request):
    type = request.GET.get('type', '')
    print(type)
    if type == "com":
        time.sleep(2)
        return JsonResponse({"classname": "com"})
    return JsonResponse({})