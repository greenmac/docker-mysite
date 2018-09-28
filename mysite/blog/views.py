from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType

# each_page_blogs_num = 2  # 每2篇進行分頁

# Create your views here.
def blogList(request):
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 獲取當前頁碼
    # 獲取前後各兩頁的頁碼
    page_range = list(range(max(current_page_num - 2, 1), min(paginator.num_pages + 1, current_page_num + 3)))
    # 加上省略標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)

def blogDetail(request, blog_pk):
    context = {}
    context['blog']= get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)

def blogsWithType(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_types'] = BlogType.objects.all()
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1) # 獲取url的頁面參數(GET請求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number # 獲取當前頁碼
    # 獲取前後各兩頁的頁碼
    page_range = list(range(max(current_page_num - 2, 1), min(paginator.num_pages + 1, current_page_num + 3)))
    # 加上省略標記
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首頁和尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    context = {}
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()



















    return render_to_response('blog/blogs_with_type.html', context)