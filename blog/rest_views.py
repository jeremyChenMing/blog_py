from .models import *
from rest_framework.decorators import api_view
from rest_framework import views
from .serializers import UserSerializer
# ArticalSerializer, CommentSerializer, FriendSerializer, PageNumberPagination
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
#
#
from rest_framework import permissions
from rest_framework_simplejwt import authentication

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        print(attrs)
        try:
            data = super().validate(attrs)
            # 默认行为
            # refresh = self.get_token(self.user)
            # data['refresh'] = str(refresh)
            # data['access'] = str(refresh.access_token)

            data['username'] = self.user.username
            data['id'] = self.user.id
            data['web_site'] = self.user.web_site
            data['avatar'] = self.user.avatar
            data['phone'] = self.user.phone
            del data['refresh']
            # del data['access']
            return data
        except:
            return {'code': '400', 'msg': '账户或者密码错误'}


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TestView(views.APIView):
    # 指定是否有权限访问
    # permission_classes = (permissions.IsAuthenticated, )
    # permission_classes = ()
    # authentication_classes = (authentication.JWTAuthentication,)
    # authentication_classes = ()

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)
        user = User.objects.get(id=access['user_id'])
        print(user)
        serliear = UserSerializer(user)
        print(serliear.data['id'])
        return Response(serliear.data, status=200)


# 创建用户
class create_user(views.APIView):
    # permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        has = User.objects.filter(username=request.data['username']).first()
        if has:
            return Response({'msg': '该用户名已经注册', 'code': 404}, status=200)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.create(request.data)
            User.objects.create_user(**request.data)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=500)


# 用户详情、删除、更新
class users(views.APIView):
    # permission_classes = ()
    # 默认启用jwt token
    # authentication_classes = ()

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            user = User.objects.get(id=access['user_id'])
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)

    def put(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            user = User.objects.get(id=access['user_id'])
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)

    def delete(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            user = User.objects.get(id=access['user_id'])
            user.delete()
            return Response({}, status=200)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)


# # 文章列表
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def artical_list(request):
#     if request.method == 'GET':
#         query = request.query_params
#         if query['group'] == 'time':
#             time_check = query['time']
#             if time_check == 'down':
#                 time_check = '-created_at'
#             else:
#                 time_check = 'created_at'
#             articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(time_check)
#
#         elif query['group'] == 'hot':
#             hot = query['hot']
#             if hot == 'down':
#                 hot = 'hots'
#             else:
#                 hot = '-hots'
#             articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(hot)
#
#         elif query['group'] == 'nice':
#             nice = query['nice']
#             if nice == 'down':
#                 nice = 'nices'
#             else:
#                 nice = '-nices'
#             articals = Artical.objects.filter(title__contains=query['word'], classify__contains=query['classify']).order_by(nice)
#         # 率选某一用户发表过的文章
#         elif query['group'] == 'artical':
#             user_id = query['id']
#             articals = Artical.objects.filter(user_id=user_id)
#
#         page_obj = PageNumberPagination()
#         page_data = page_obj.paginate_queryset(articals, request)
#         ser_obj = ArticalSerializer(page_data, many=True)
#         return page_obj.get_paginated_response(ser_obj.data)
#
#     elif request.method == 'POST':
#         user_detail = User.objects.get(pk=request.data['user_id'])
#         request.data['user'] = user_detail
#         print(request.data)
#         serializer = ArticalSerializer(data=request.data)
#         if serializer.is_valid():
#             # serializer.create(request.data)
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=500)
#
#
# # 文章详情
# @api_view(['GET', 'PUT', 'DELETE'])
# @csrf_exempt
# def artical_detail(request, pk):
#     try:
#         artical = Artical.objects.get(pk=pk)
#     except:
#         return Response(status=404)
#
#     if request.method == 'GET':
#         req = {
#             "hots": artical.hots + 1,
#             # "followed": False
#         }
#         serializer = ArticalSerializer(artical, data=req)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)
#         return Response(serializer.errors, status=500)
#
#     elif request.method == 'PUT':
#         serializer = ArticalSerializer(artical, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         artical.delete()
#         return Response({}, status=200)
#
#


# # 评论列表
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def comment_list(request):
#     if request.method == 'GET':
#         # artical_id = request.query_params['artical_id']
#         artical_id = request.GET.get('artical_id')
#         user_id = request.GET.get('user_id')
#         if artical_id:
#             ar = Artical.objects.filter(id=artical_id).first()
#             if ar:
#                 comments = ar.artical_comment.all()
#                 serializer = CommentSerializer(comments, many=True)
#                 p1 = list()
#                 p2 = list()
#                 for x in serializer.data:
#                     if x['to_comment']:
#                         p2.append(x)
#                     else:
#                         x['comment_children'] = list()
#                         p1.append(x)
#
#                 for a in p2:
#                     for b in p1:
#                         if b['id'] == a['to_comment']:
#                             b['comment_children'].append(a)
#                 return Response({'items': p1}, status=200)
#             return Response({"items": []}, status=200)
#         elif user_id:
#             ur = User.objects.filter(id=user_id).first()
#             if ur:
#                 comments = ur.comment_user.all()
#                 serializer = CommentSerializer(comments, many=True)
#                 for n in serializer.data:
#                     if n['to_comment']:
#                         select_artical = Comment.objects.filter(id=n['to_comment']).first()
#                         serializer_select = CommentSerializer(select_artical)
#                         n['to_comment_dict'] = {"nickname": serializer_select.data['belong_user']['nickname'], "id": serializer_select.data['belong_user']['id']}
#                 return Response({"items": serializer.data}, status=200)
#             return Response({"items": []}, status=200)
#         return Response(status=500)
#
#     elif request.method == 'POST':
#         artical_obj = Artical.objects.get(id=request.data['belong_artical'])
#         user_obj = User.objects.get(id=request.data['belong_user'])
#         request.data['belong_artical'] = artical_obj
#         request.data['belong_user'] = user_obj
#         serializer = CommentSerializer(data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.create(request.data)
#             return Response({}, status=200)
#         return Response(serializer.errors, status=500)
#
# # 点赞与取消点赞
# @api_view(['POST'])
# @csrf_exempt
# def handle_nice(request):
#     try:
#         article = Artical.objects.get(pk=request.data['artical_id'])
#     except Artical.DoseNotExist:
#         return Response(status=404)
#
#     if request.data['action'] == 'like':
#         req = {
#             'user_like': article.user_like,
#             'nices': article.nices
#         }
#         req['user_like'].add(request.data['user_id'])
#         req['nices'] += 1
#         serializer = ArticalSerializer(article, data=req, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({}, status=200)
#         return Response(serializer.errors, status=500)
#     else:
#         req = {
#             'user_like': article.user_like,
#             'nices': article.nices
#         }
#         req['user_like'].remove(request.data['user_id'])
#         req['nices'] -= 1
#         serializer = ArticalSerializer(article, data=req, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({}, status=200)
#         return Response(serializer.errors, status=500)
#
#
# # 个人点赞数量统计
# @api_view(['GET'])
# @csrf_exempt
# def nice_count(request, pk):
#     try:
#         user_detail = User.objects.get(pk=pk)
#     except User.DoseNotExist:
#         return Response(status=404)
#     articals = user_detail.like_user.all()
#     serializer = ArticalSerializer(articals, many=True)
#     return Response({'items': serializer.data, 'count': len(serializer.data)}, status=200)
#
#
# # 用户登录后是否有关注
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def follow_count(request, pk):
#     if request.method == 'GET':
#         detail = FriendShip.objects.filter(followed_id=pk, follower_id=request.query_params['id']).first()
#         all = FriendShip.objects.all()
#         serializer = FriendSerializer(all)
#         print(serializer.data)
#         if detail:
#             return Response({'follow': True})
#         else:
#             return Response({'follow': False})
#
#     elif request.method == 'POST':
#         detail = FriendShip.objects.filter(follower_id=pk, followed_id=request.data['follower']).first()
#         if detail:
#             detail.delete()
#             return Response({}, status=200)
#         else:
#             request.data['followed_id'] = request.data['follower']
#             request.data['follower_id'] = pk
#             del request.data['follower']
#             print(request.data)
#             serializer = FriendSerializer(data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.create(request.data)
#                 return Response(serializer.data, status=200)
#             return Response(serializer.errors, status=500)
#
# # 登录着粉丝查询
# @api_view(['GET'])
# @csrf_exempt
# def friend_fan(request, pk):
#     try:
#         user_detail = User.objects.get(pk=pk)
#     except User.DoseNotExist:
#         return Response(status=404)
#     followed_user = user_detail.followed.all()
#     follower_user = user_detail.follower.all()
#     serializer_followed = ArticalSerializer(followed_user, many=True)
#     serializer_follower = FriendSerializer(follower_user, many=True)
#     return Response({
#         'follower': serializer_follower.data,
#         'followed': serializer_followed.data,
#     }, status=201)
#
