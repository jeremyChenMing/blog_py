from django.urls import path
from . import views
from . import rest_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index),
    path('example', views.example),
    path('postexam', views.postexam),
    path('putexam/<str:put_id>', views.putexam),
    path('delexam/<str:del_id>', views.delexam),
    path('detail/<int:page_id>', views.detail, name='detail_page'),
    path('details/<str:page_id>', views.details),
    path('edit/<int:page_id>', views.edit, name='edit_page'),
    # re_path(r'^edit/(?P<page_id>[0-9]+)$', views.edit, name='edit_page'),
    path('edit/edit_action', views.edit_action, name="edit_action"),
    path('artical_list/<str:user_id>', views.artical_user),


    path('users', views.user_list),
    path('upload', views.upload_avatar),
    path('login', views.login),
    path('create_user', views.create_user),
    path('user_detail/<str:user_id>', views.get_user),
    path('user_edit/<str:user_id>', views.edit_user),
    # 评论
    path('comments', views.comment_list),
    path('comments_user', views.comment_user),
    path('create_comment', views.post_comment),
    # 点赞
    path('handle_nice', views.post_nice),
    path('get_nice/<str:user_id>', views.get_nice_person),
    # 关注
    path('follow', views.post_follow),
    path('fans/<str:user_id>', views.get_fans),
    path('followers/<str:user_id>', views.get_followers),
    # 游戏记录
    path('record', views.post_game),
    path('record_list', views.get_game),
    # 测试接口
    path('test_env', views.back_env),

    path('articals', rest_views.artical_list),
    path('articals/<str:pk>', rest_views.artical_detail),
    path('user_info', rest_views.user_column),
    path('user_info/<str:pk>', rest_views.user_info),
    path('comment_info', rest_views.comment_list),
]