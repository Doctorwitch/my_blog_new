from celery import Celery
from django.conf import settings
from django.core.mail import send_mail

# 在任务处理者一端加
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
django.setup()

# 创建celery类的对象

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/2')

# 定义任务函数


@app.task
def send_register_active_email(to_mail, name, token):
    subject = '北方博客注册邮件'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_mail]
    html_msg = '<h1>%s,欢迎您注册北方博客账号</h1><p>请点击以下链接激活您的账户</P><a href="http://127.0.0.1:8000/active/%s">http://127.0.0.1:8000/active/%s</a>' % (
    name, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_msg)



