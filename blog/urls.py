from django.urls import path
from . import views

# start with blog
urlpatterns = [
    # 博客根目录
    path('', views.blog_list, name='blog_list'),
    # 博客详情页面，http://localhost:8000/blog/blog_pk
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    # 博客按类型分类页面，http://localhost:8000/blog/type/blog_pk
    path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
    # 博客按日期分类页面，http://localhost:8000/blog/date/year/month
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]