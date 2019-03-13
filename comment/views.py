from django.shortcuts import render
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from comment.models import CommentManage
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class Board(LoginRequiredMixin, View):
    '''显示评论页面'''
    def get(self, request):
        comment = CommentManage.objects.all()
        comment_manage = comment.order_by('-creat_time')[:]
        return render(request, 'board.html', {'comment': comment_manage})

    def post(self, request):
        # 接受表单数据
        comment = request.POST.get('comment')
        comment_manage = CommentManage()
        comment_manage.user_id = request.user
        comment_manage.comment = comment
        comment_manage.save()
        return redirect(reverse('comment:board'))
