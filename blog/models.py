from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(verbose_name='博客类型', max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(verbose_name='标题', max_length=50)
    blog_type = models.ForeignKey(verbose_name='博客类型', to=BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField(verbose_name='内容')
    author = models.ForeignKey(verbose_name='作者', to=User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)  # 关联模型
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_update_time = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)

    def __str__(self):
        return '<Blog: {title}>'.format(title=self.title)

    class Meta:
        # 按创建时间降序排列
        ordering = ['-create_time']

