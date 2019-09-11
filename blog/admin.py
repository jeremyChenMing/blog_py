from django.contrib import admin
from . import models
# Register your models here.


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'phone', 'created_at', 'password')

# class ArticalAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('belong_artical', 'belong_user', 'word')
#
#
# class FriendAdmin(admin.ModelAdmin):
#     list_display = ('followed', 'follower')
#
#
# class GameAdmin(admin.ModelAdmin):
#     list_display = ('kilometer', 'user')


admin.site.register(models.User, UsersAdmin)
# admin.site.register(models.Artical, ArticalAdmin)
# admin.site.register(models.Comment, CommentAdmin)
# admin.site.register(models.FriendShip, FriendAdmin)
# admin.site.register(models.Game, GameAdmin)
