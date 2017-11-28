from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from escort.app.models import News
from escort.ocs.models import Task


def index(request):
    return render(request, 'app/index.html')
    # return HttpResponse("OK")


def news(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 25)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'app/news.html', {'news_list': news})


def documents(request):
    return render(request, 'app/docments.html')


def tasks(request):
    list_of_tasks = Task.objects.filter(finish_rate__lt=100).order_by('finish_rate', 'deadline_date')
    context_dict = {'tasks': list_of_tasks}
    return render(request, 'app/tasks.html', context_dict)


def videos(request):
    return render(request, 'app/videos.html')


def statistics(request):
    return render(request, 'app/statistics.html')


def map(request):
    return render(request, 'app/map.html')


def center(request):
    return render(request, 'app/center.html')
