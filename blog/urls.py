from django.urls import path
from . import views

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
    path('upload/<str:user_id>', views.upload_avatar),
    path('login', views.login),
    path('create_user', views.create_user),
    path('user_detail/<str:user_id>', views.get_user),
    path('user_edit/<str:user_id>', views.edit_user),
    # 评论
    path('comments', views.comment_list),
    path('comments_user', views.comment_user),
    path('create_comment', views.post_comment),
]