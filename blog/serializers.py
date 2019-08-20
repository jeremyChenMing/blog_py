from rest_framework import serializers
from rest_framework import pagination
from .models import Artical, User
from rest_framework.response import Response


# 对应USER外键的关系, 一对一，多对多
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'id', 'user_name']


class ArticalSerializer(serializers.ModelSerializer):
    user = TrackSerializer(read_only=True)
    user_like = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Artical
        fields = ['id', 'title', 'classify', 'hots', 'nices', 'content', 'user', 'user_like', 'created_at', 'updated_at']


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