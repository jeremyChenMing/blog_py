from .models import *
from rest_framework.decorators import api_view
from .serializers import ArticalSerializer, UserSerializer, CommentSerializer, PageNumberPagination
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


# 文章列表
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
        # 率选某一用户发表过的文章
        elif query['group'] == 'artical':
            user_id = query['id']
            articals = Artical.objects.filter(user_id=user_id)

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


# 文章详情
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


# 获取用户
@api_view(['GET', 'POST'])
@csrf_exempt
def user_column(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        has = User.objects.filter(user_name=request.data['user_name']).first()
        if has:
            return Response({'msg': '该用户名已经注册', 'code': 404}, status=200)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=500)


# 用户详情
@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def user_info(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoseNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response({}, status=200)


# 评论列表
@api_view(['GET', 'POST'])
@csrf_exempt
def comment_list(request):
    if request.method == 'GET':
        # artical_id = request.query_params['artical_id']
        artical_id = request.GET.get('artical_id')
        user_id = request.GET.get('user_id')
        if artical_id:
            ar = Artical.objects.filter(id=artical_id).first()
            if ar:
                comments = ar.artical_comment.all()
                serializer = CommentSerializer(comments, many=True)
                p1 = list()
                p2 = list()
                for x in serializer.data:
                    if x['to_comment']:
                        p2.append(x)
                    else:
                        x['comment_children'] = list()
                        p1.append(x)

                for a in p2:
                    for b in p1:
                        if b['id'] == a['to_comment']:
                            b['comment_children'].append(a)
                return Response({'items': p1}, status=200)
            return Response({"items": []}, status=200)
        elif user_id:
            print('用户')
            ur = User.objects.filter(id=user_id).first()
            if ur:
                comments = ur.comment_user.all()
                serializer = CommentSerializer(comments, many=True)
                for n in serializer.data:
                    if n['to_comment']:
                        select_artical = Comment.objects.filter(id=n['to_comment']).first()
                        serializer_select = CommentSerializer(select_artical)
                        n['to_comment_dict'] = {"nickname": serializer_select.data['belong_user']['nickname'], "id": serializer_select.data['belong_user']['id']}
                return Response({"items": serializer.data}, status=200)
            return Response({"items": []}, status=200)
        return Response(status=500)

    elif request.method == 'POST':
        artical_obj = Artical.objects.get(id=request.data['belong_artical'])
        user_obj = User.objects.get(id=request.data['belong_user'])
        request.data['belong_artical'] = artical_obj
        request.data['belong_user'] = user_obj
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response({}, status=200)
        return Response(serializer.errors, status=500)
