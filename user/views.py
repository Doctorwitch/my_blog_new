from django.shortcuts import render
from django.views.generic import View
from article.models import ArticleManage
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from celery_tasks.tasks import send_register_active_email
from user.models import User
from django.contrib.auth import authenticate, login, logout
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
import re


# Create your views here.


class Register(View):
    '''注册页面'''
    def get(self, request):
        return render(request, 'base_register.html')

    def post(self, request):
        # 接收数据
        name = request.POST.get('name')
        password = request.POST.get('pwd')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        # 用户名不允许重复
        try:
            User.objects.get(username=name)
            return render(request, 'base_register.html', {'errmsg': '用户名已存在'})
        except User.DoesNotExist:
            pass
        # 数据不完整
        if not all([name, password, email]):
            return render(request, 'base_register.html', {'errmsg': '数据不完整'})
        # 邮箱是否合法
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return render(request, 'base_register.html', {'errmsg': '邮箱格式不合法'})
        # 密码是否一致
        if password_confirm != password:
            return render(request, 'base_register.html', {'errmsg': '密码不一致'})
        # 是否同意协议
        if allow != '1':
            return render(request, 'base_register.html', {'errmsg': '虽然没用，但是流程还是要走的啊，快点同意py协议！'})
        # 进行业务处理：进行用户注册
        user = User.objects.create_user(name, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接：激活链接中需要包含用户的身份信息http://127.0.0.1:8000/active/用户id
        # 激活链接中的用户信息需要加密,生成token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()
        # 使用celery发送激活邮件
        send_register_active_email.delay(email, name, token)
        # 返回应答，回答首页
        return redirect(reverse('user:index'))


class Active(View):
    '''用户激活账号'''
    def get(self, request, token):
        '''进行用户激活'''
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 返回应答,跳转到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return render(request, 'base_register.html', {'errmsg': '激活链接已过期，请重新获取'})


class Login(View):
    def get(self, request):
        return render(request, 'base_login.html')

    def post(self, request):
        # 接受数据
        name = request.POST.get('name')
        password = request.POST.get('pwd')
        # 登录校验
        if not all([name, password]):
            return render(request, 'base_login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=name, password=password)
        if user is not None:
            if user.is_active:
                # 用户已激活
                login(request, user)
                next_url = request.GET.get('next', reverse('user:index'))
                return redirect(next_url)
            else:
                # 用户未激活
                return render(request, 'base_login.html', {'errmsg': '用户未激活，请检查注册邮箱并点击激活链接激活账户'})
        else:
            return render(request, 'base_login.html', {'errmsg': '用户名或密码错误，请检查输入是否正确或点击立即注册，注册新用户'})


class Logout(View):
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)
        # 跳转到首页
        return redirect(reverse('user:index'))


class Index(View):
    def get(self, request):
        '''首页'''
        article = ArticleManage.objects.all()
        hot = ArticleManage.objects.order_by('-read_times')[:5]
        return render(request, 'index.html', {'article': article, 'hot': hot})


class About(View):
    def get(self, request):
        return render(request, 'about.html')





