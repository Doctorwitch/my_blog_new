from django.db import models
from db.base_model import BaseModel

# Create your models here.


class CommentManage(BaseModel):
    '''博客评论管理类'''
    user_id = models.ForeignKey('user.User', verbose_name='评论用户')
    sum_up = models.IntegerField(default=0, verbose_name='点赞数')
    comment = models.TextField(max_length=500)
    parent_comment = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        '''博客评论类'''
        db_table = 'comment_manage'
        verbose_name = '博客评论类'
        verbose_name_plural = verbose_name





