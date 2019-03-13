from django.db import models
from db.base_model import BaseModel

# Create your models here.


class MoodManage(BaseModel):
    '''心情管理'''
    title = models.CharField(max_length=128, verbose_name='心情标题')
    cont = models.CharField(max_length=512, verbose_name='心情内容')

    class Meta:
        db_table = 'mood_manage'
        verbose_name = '心情管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

