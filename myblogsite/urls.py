"""myblogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 家目录，localhost:8000
    path('', views.home, name='home'),
    # 后台管理，localhost:8000/admin/
    path('admin/', admin.site.urls),
    # 为了使用富文本编辑器，并且上传图片
    path('ckeditor', include('ckeditor_uploader.urls')),
    # 博客根目录，localhost:8000/blog/
    path('blog/', include('blog.urls')),
    # 登录页面
    path('login/', views.login, name='login'),
    # 评论根目录
    path('comment/', include('comment.urls')),
]

# 为了使用富文本编辑器，并且上传图片
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
