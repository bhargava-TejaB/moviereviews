from django.shortcuts import render
from .models import News

def news(request):
    n = News.objects.all().order_by("-date")
    return render(request, 'news.html', {'news': n})