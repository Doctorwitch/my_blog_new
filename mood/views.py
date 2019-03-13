from django.shortcuts import render
from django.views.generic import View
from mood.models import MoodManage

# Create your views here.


class Mood(View):
    def get(self, request):
        moods = MoodManage.objects.all()
        return render(request, 'mood.html', {'moods': moods})




