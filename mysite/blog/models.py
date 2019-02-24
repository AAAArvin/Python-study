from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import *

# Create your models here.

#博客分类
class BlogType(models.Model):
    type_name = models.CharField('分类', max_length=15)

    def __str__(self):
        return self.type_name

#博客模型
class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField('标题', max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField('正文')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    last_updated_time = models.DateTimeField('最后修改时间', auto_now=True)

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-created_time']