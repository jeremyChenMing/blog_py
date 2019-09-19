from .models import *
from rest_framework import views
from .serializers import UserSerializer, ArticalSerializer, PageNumberPagination, CommentSerializer, FriendSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
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


# 文章
class articalObject(views.APIView):
    # 创建文章
    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            request.data['user_id'] = access['user_id']
            serializer = ArticalSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(request.data)
                # Artical.objects.create(**request.data)
                # serializer.save()
                return Response({}, status=200)
            return Response(serializer.errors, status=500)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)

    def put(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            artical = Artical.objects.get(pk=request.data['artical_id'])
            request.data['user_id'] = access['user_id']
            serializer = ArticalSerializer(artical, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=200)
            return Response(serializer.errors, status=500)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)

    def delete(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            artical = Artical.objects.get(pk=request.data['artical_id'])
            artical.delete()
            return Response({}, status=200)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)


# 文章列表
class articalGet(views.APIView):
    authentication_classes = ()

    def get(self, request):
        query = request.query_params
        if 'artical_id' in query:
            artical = Artical.objects.get(pk=query['artical_id'])
            req = {
                "hots": artical.hots + 1,
                # "followed": False
            }
            serializer = ArticalSerializer(artical, data=req)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=500)

        else:
            if query['group'] == 'time':
                time_check = query['time']
                if time_check == 'down':
                    time_check = '-created_at'
                else:
                    time_check = 'created_at'
                articals = Artical.objects.filter(title__contains=query['word'],
                                                  classify__contains=query['classify']).order_by(time_check)

            elif query['group'] == 'hot':
                hot = query['hot']
                if hot == 'down':
                    hot = 'hots'
                else:
                    hot = '-hots'
                articals = Artical.objects.filter(title__contains=query['word'],
                                                  classify__contains=query['classify']).order_by(hot)

            elif query['group'] == 'nice':
                nice = query['nice']
                if nice == 'down':
                    nice = 'nices'
                else:
                    nice = '-nices'
                articals = Artical.objects.filter(title__contains=query['word'],
                                                  classify__contains=query['classify']).order_by(nice)
            # 率选某一用户发表过的文章
            elif query['group'] == 'artical':
                user_id = query['id']
                articals = Artical.objects.filter(user_id=user_id)

            page_obj = PageNumberPagination()
            page_data = page_obj.paginate_queryset(articals, request)
            ser_obj = ArticalSerializer(page_data, many=True)
            return page_obj.get_paginated_response(ser_obj.data)


# 获取某一用户下的所有文章
class articalUser(views.APIView):

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            auther = User.objects.filter(pk=access['user_id']).first()
            if auther:
                articals = auther.artical_user.all()
                serializer = ArticalSerializer(articals, many=True)
                return Response({'count': len(serializer.data), 'items': serializer.data}, status=200)
            return Response({'count': 0, 'items': []}, status=200)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)


# 评论列表列表
class commentGet(views.APIView):
    authentication_classes = ()

    def get(self, request):
        query = request.query_params
        artical_obj = Artical.objects.filter(pk=query['artical_id']).first()
        all_comment = artical_obj.artical_comment.all()
        serializer = CommentSerializer(all_comment, many=True)
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


# 创建评论
class commentObj(views.APIView):

    def post(self, request):
        print(request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            # serializer.save()
            return Response({}, status=200)
        return Response(serializer.errors, status=500)

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        try:
            access = AccessToken(access_str)
            auther = User.objects.filter(pk=access['user_id']).first()
            if auther:
                comments = auther.comment_user.all()
                serializer = CommentSerializer(comments, many=True)
                for n in serializer.data:
                    if n['to_comment']:
                        select_artical = Comment.objects.filter(pk=n['to_comment']).first()
                        serializer_select = CommentSerializer(select_artical)
                        n['to_comment_dict'] = {
                            "nickname": serializer_select.data['belong_user']['nickname'],
                            "id": serializer_select.data['belong_user']['id']
                        }
                return Response({"items": serializer.data}, status=200)
        except:
            return Response({'code': 400, 'msg': 'token错误'}, status=404)


# 点赞
class niceObj(views.APIView):

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)
        article = Artical.objects.get(pk=request.data['artical_id'])
        req = {
            'user_like': article.user_like,
            'nices': article.nices
        }
        if request.data['action'] == 'like':
            req['user_like'].add(access['user_id'])
            req['nices'] += 1
            serializer = ArticalSerializer(article, data=req, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=200)
            return Response(serializer.errors, status=500)
        else:
            req['user_like'].remove(access['user_id'])
            req['nices'] -= 1
            serializer = ArticalSerializer(article, data=req, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=200)
            return Response(serializer.errors, status=500)

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)
        try:
            user_detail = User.objects.get(pk=access['user_id'])
        except User.DoseNotExist:
            return Response(status=404)
        articals = user_detail.like_user.all()
        serializer = ArticalSerializer(articals, many=True)
        return Response({'items': serializer.data, 'count': len(serializer.data)}, status=200)


# 点赞
class followObj(views.APIView):

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)

        detail = FriendShip.objects.filter(followed_id=request.data['follower'], follower_id=access['user_id']).first()
        req = {
            'followed_id': request.data['follower'],
            'follower_id': access['user_id']
        }
        if detail:
            detail.delete()
            return Response({}, status=200)
        else:
            serializer = FriendSerializer(data=req, partial=True)
            if serializer.is_valid():
                serializer.create(req)
                return Response({}, status=200)
            return Response(serializer.errors, status=500)


# 获取是否关注
class followGet(views.APIView):
    authentication_classes = ()

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)
        query = request.query_params
        detail = FriendShip.objects.filter(followed_id=query['follower'], follower_id=access['user_id']).first()
        if detail:
            return Response({'follow': True})
        else:
            return Response({'follow': False})


# 获取登录人关注的人和粉丝
class followList(views.APIView):
    authentication_classes = ()

    def get(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        access_str = auth[7:]
        access = AccessToken(access_str)
        try:
            user_detail = User.objects.get(pk=access['user_id'])
        except:
            return Response(status=404)
        followed_user = user_detail.followed.all()
        follower_user = user_detail.follower.all()
        serializer_followed = ArticalSerializer(followed_user, many=True)
        serializer_follower = FriendSerializer(follower_user, many=True)
        return Response({
            'follower': serializer_follower.data,
            'followed': serializer_followed.data,
        }, status=200)
        # return Response({'follow': False})
