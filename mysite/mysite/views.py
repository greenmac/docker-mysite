from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import getSevenDaysReadDate
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = getSevenDaysReadDate(blog_content_type)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    return render_to_response('home.html', context)