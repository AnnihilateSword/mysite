from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.db import models
from django.utils import timezone


class ReadNum(models.Model):
    read_num = models.IntegerField(verbose_name='文章阅读数量', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadNumExpandMethod:
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=ct, object_id=self.pk).read_num
            return read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0


class ReadDetail(models.Model):
    """
        记录更加详细的信息
    """
    date = models.DateField(verbose_name='日期', default=timezone.now)
    read_num = models.IntegerField(verbose_name='文章阅读数量', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

