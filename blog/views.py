from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings
from django.db.models import Count  # 用于统计
from read_statistics.utils import read_statistics_once_read
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


def get_blog_list_common_data(request, blogs_all_list) -> dict:
    """
        获取博客列表常用数据
    """
    # 每 EACH_PAGE_BLOGS_NUM 页进行分页
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUM)
    # 获取url的页面参数（GET请求），不一定是整型
    # 例如：localhost:8000/blog/?page=1
    # 例如：href="?page={{ page_of_blogs.previous_page_number }}"
    page_num = request.GET.get('page', 1)
    # django提供了处理，就算这里值的 'a' 等其他字符，会返回1，无效的会返回第一页
    # 是范围内数值的话，就正常返回
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 判断页面范围，获取当前页面页码前后范围！！！
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages > page_range[-1] > 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                                         create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {
        'blogs': page_of_blogs.object_list,
        'page_range': page_range,
        'page_of_blogs': page_of_blogs,
        'blog_types': BlogType.objects.annotate(blog_count=Count('blog')),  # 获取博客分类的对应博客数量
        'blog_dates': blog_dates_dict,
    }
    return context


def blog_list(request):
    """
        博客列表
    """
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    """
        博客按类型分类
    """
    # 先看博客类型表中是否存在该类型名称，不存在则 404
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 筛选
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    """
        博客按日期分类
    """
    # 筛选【通过年月】
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    # 用 id=xxx 或 pk=xxx
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 更新博客文章阅读数量，配合 Cookie
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = {
        'blog': blog,
        'previous_blog': Blog.objects.filter(create_time__gt=blog.create_time).last(),
        'next_blog': Blog.objects.filter(create_time__lt=blog.create_time).first(),
        'comments': comments,
    }
    response = render(request, 'blog/blog_detail.html', context)
    # 用 Cookie 保存一些数据，注意：Cookie 会有一个有效期，过一段时间会失效，单位是 (s)
    # max_age，expires 不能一起使用
    # response.set_cookie('blog_%s_read' % blog_pk, 'true', max_age=30, expires=datetime)
    response.set_cookie(read_cookie_key, 'true')  # 阅读 cookie 标记
    return response
