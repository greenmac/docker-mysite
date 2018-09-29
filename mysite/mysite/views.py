import datetime
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from read_statistics.utils import getSevenDaysReadDate, getTodayHotDate, getYesterdayHotDate
from blog.models import Blog

def getSevendayHotDate():
    today = timezone.now().date()
    date = today-datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = getSevenDaysReadDate(blog_content_type)

    # 獲取7天熱門文章的緩存數據
    seven_days_hot_date = cache.get('seven_days_hot_date')
    if seven_days_hot_date is None:
        seven_days_hot_date = getSevendayHotDate()
        cache.set('seven_days_hot_date', seven_days_hot_date, 3600)
        print('calc')
    else:
        print('use caches')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_date'] = getTodayHotDate(blog_content_type)
    context['yesterday_hot_date'] = getYesterdayHotDate(blog_content_type)
    context['seven_days_hot_date'] = seven_days_hot_date
    return render_to_response('home.html', context)