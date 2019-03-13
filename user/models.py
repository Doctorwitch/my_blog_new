from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser, BaseModel):
    '''继承内置用户模块'''
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



