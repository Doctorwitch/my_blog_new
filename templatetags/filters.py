# 自定义过滤器
# 过滤器本质是一个Python函数
from django.template import Library

register = Library()


@register.filter
def mod(num):
    '''判断num是否为偶数'''
    return num%2 == 0


