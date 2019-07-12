from blog.utils import models
# import datetime

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    prefix = models.CharField(max_length=2, default='86')
    web_site = models.CharField(max_length=100)
    agree = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True)

    def __str__(self):
        return self.user_name


class Artical(models.Model):
    title = models.CharField(max_length=102, default='默认标题')
    classify = models.CharField(max_length=20, default='')
    hots = models.IntegerField(default=0)
    # user_id = models.CharField(max_length=36)
    content = models.TextField(null=True)
    user = models.ForeignKey(User, null=True, related_name="artical", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    word = models.TextField(null=False)
    # 评论文章的id
    belong_artical = models.ForeignKey(Artical, null=True, related_name="artical_comment", on_delete=models.CASCADE)
    # 评论文章的人的id
    belong_user = models.ForeignKey(User, null=True, related_name="comment_user", on_delete=models.CASCADE)
    # 对谁进行评论者的id
    to_comment = models.CharField(max_length=36, default='')

    def __str__(self):
        return self.word

