from datetime import datetime

from django.db import models
from djangoblog import settings
from django.utils import timezone

from DjangoUeditor.models import UEditorField

# Create your models here.

STATUS = {
    0: u'发表',
    1: u'草稿',
    2: u'丢弃',
}

ARTICLE_FROM = {
    0: u'原创',
    1: u'转载',
}

IS_READ = {
    0: u'未读',
    1: u'已读',
}


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'类型名称')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
    update_time = models.DateTimeField(verbose_name=u'修改时间',blank=True,null=True)

    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name
        ordering = ['rank','-create_time']

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'作者')
    category = models.ForeignKey(Category,verbose_name=u'类型')
    title = models.CharField(max_length=50,verbose_name=u'标题')
    #en_title = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'英文名')
    article_from = models.IntegerField(default=0,choices=ARTICLE_FROM.items(),verbose_name=u'文章来源')
    summary = models.TextField(verbose_name=u'摘要')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'标签', help_text=u'用逗号分隔')
    content = UEditorField(verbose_name=u'正文', toolbars='full', width='600', height='300', imagePath='article/ueditor/',filePath='article/ueditor',default='')
    reading_num = models.IntegerField(default=0,verbose_name=u'阅读量')
    comment_num = models.IntegerField(default=0,verbose_name=u'评论数')
    like_num = models.IntegerField(default=0,verbose_name=u'点赞数')

    is_top = models.BooleanField(default=False,verbose_name=u'是否置顶')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'文章状态')

    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间', blank=True, null=True)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article-view', args=(self.en_title,))

    def get_tags(self):
        tags_list = self.tags.split(',')
        while '' in tags_list:
            tags_list.remove('')
        tags_list = tags_list[0:3]

        return tags_list

    def get_category(self):
        return self.category

    def __str__(self):
        return self.title



class Link(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'链接名')
    url = models.URLField(max_length=40, verbose_name=u'链接地址')
    rank = models.IntegerField(default=0, verbose_name=u'排序')

    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间', blank=True, null=True)

    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Notification(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    text = models.TextField(verbose_name=u'内容')
    url = models.CharField(max_length=200, verbose_name=u'连接', null=True, blank=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  default=None, blank=True, null=True,
                                  related_name='from_user_notification_set',
                                  verbose_name=u'发送者')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_notification_set', verbose_name=u'接收者')
    type = models.CharField(max_length=20, verbose_name=u'类型', null=True, blank=True)
    is_read = models.IntegerField(default=0, choices=IS_READ.items(), verbose_name=u'是否读过')

    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    update_time = models.DateTimeField(verbose_name=u'修改时间', blank=True, null=True)

    class Meta:
        ordering = ['-create_time']
        verbose_name = u'消息'
        verbose_name_plural = verbose_name
