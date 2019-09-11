from rest_framework import serializers
from rest_framework import pagination
from .models import User
# Artical, Comment, FriendShip
from rest_framework.response import Response


# 分页
class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 10  # 指定每页显示多少条数据
    page_size_query_param = 'page_size'  # URL参数中每页显示条数的参数
    page_query_param = 'page'  # URL中页码的参数
    max_page_size = None  # 每页最多显示多少条数据

    def get_paginated_response(self, data):
        return Response({
            # 'links': {
            #     'next': self.get_next_link(),
            #     'previous': self.get_previous_link()
            # },
            'count': self.page.paginator.count,
            'items': data
        })


# 文章序列化 --- 对应USER外键的关系, 一对一，多对多
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'id', 'user_name']


# 文章序列化
# class ArticalSerializer(serializers.ModelSerializer):
#     user = TrackSerializer(read_only=True)
#     user_like = TrackSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Artical
#         fields = ['id', 'title', 'classify', 'hots', 'nices', 'content', 'user', 'user_like', 'created_at', 'updated_at']


# 用户序列化
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'nickname', 'web_site', 'avatar', 'id', 'phone', 'created_at', 'updated_at']

        # fields = ['username', 'email', 'id', 'phone', 'web_site', 'avatar', 'created_at', 'updated_at', 'prefix', 'agree']


# # 文章序列化
# class TrackArticalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Artical
#         fields = ['id', 'title', 'created_at', 'updated_at']
#
#
# # 评论列表
# class CommentSerializer(serializers.ModelSerializer):
#     belong_user = TrackSerializer(read_only=True)
#     belong_artical = TrackArticalSerializer(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['word', 'to_comment', 'id', 'belong_user', 'belong_artical', 'created_at', 'updated_at']
#
#
# # 关注
# class FriendSerializer(serializers.ModelSerializer):
#     followed = TrackSerializer(read_only=True)
#     follower = TrackSerializer(read_only=True)
#
#     class Meta:
#         model = FriendShip
#         fields = ['followed', 'follower', 'created_at', 'updated_at', 'id']