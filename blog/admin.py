from django.contrib import admin
from . import models
# Register your models here.


class ArticalAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'nickname', 'phone', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('belong_artical', 'belong_user', 'word')


admin.site.register(models.Artical, ArticalAdmin)
admin.site.register(models.User, UsersAdmin)
admin.site.register(models.Comment, CommentAdmin)