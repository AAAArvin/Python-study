from django.db import models
import datetime
import os
import uuid
import re
from django.contrib.auth.models import User

# Create your models here.

class Object_list_all(models.Model):
    '''
    观测目标列表总表
    '''
    STAGE_CHOICE = (
        ('current', 'current'),
        ('past', 'past'),
        ('future', 'future'),
        ('removed', 'removed'),
    )

    MODE_CHOICE = (
        ('observation', 'observation'),
        ('test', 'test'),
    )
    Object_name = models.CharField('目标名称', max_length=40)
    Object_alias_1 = models.CharField('目标别名1', max_length=30, blank=True)
    Object_alias_2 = models.CharField('目标别名2', max_length=30, blank=True)
    Obj_Type = models.CharField('目标类型', max_length=30, blank=True)
    Obj_source = models.CharField('目标来源', max_length=30, blank=True)
    Observer = models.CharField('观测者', max_length=30)
    Obs_program = models.CharField('观测项目', max_length=30, blank=True)
    Obj_RA = models.FloatField('目标赤经', max_length=30)
    Obj_DEC = models.FloatField('目标赤纬', max_length=30)
    Obj_Epoch = models.IntegerField('历元', default=2000)
    Obj_Error = models.FloatField('误差', max_length=30, default=0)
    Group_ID = models.CharField('设备群', max_length=30)
    Unit_ID = models.CharField('设备编号', max_length=30)
    Observation_type = models.CharField('观测类型', max_length=30, default='man')
    Observation_strategy = models.CharField('观测策略', max_length=30, default='pointing')
    Obs_date_begin = models.DateField('观测起始日期', max_length=30, default=datetime.date.today)
    Obs_date_end = models.DateField('观测结束日期', max_length=30)
    Obs_day_interval = models.IntegerField('观测频次', default=1)
    imgtype = models.CharField('图像类型', max_length=30, default='object')
    filter = models.CharField('波段', max_length=30)
    expdur = models.CharField('曝光时间', max_length=30)
    delay = models.CharField('曝光间隔', max_length=30, default=0)
    frmcnt = models.IntegerField('曝光幅数')
    prioriy = models.IntegerField('优先级', default=20)
    run_name = models.IntegerField('曝光轮次', default=1)
    note = models.CharField('观测说明', max_length=30, blank=True)
    Obs_stage = models.CharField('观测阶段', max_length=30, default='current', choices=STAGE_CHOICE)
    mode = models.CharField('模式', max_length=30, default='observation', choices=MODE_CHOICE)
    insert_time = models.DateField('插入时间', auto_now_add=True)

    class Meta:
        verbose_name = '观测目标列表总表'
        verbose_name_plural = verbose_name
        db_table = 'Object_list_all'
        ordering = ['prioriy']

    def __str__(self):
        return "%s" % self.Object_name


class Object_list_current(models.Model):
    '''
    待观测目标列表
    '''
    STAGED_CHOICE = (
        (0, 'scheduled'),
        (1, 'completed'),
        (2, 'canceled'),
    )
    MODE_CHOICE = (
        ('0', 'test'),
        ('1', 'observation'),
    )
    Object_ID = models.ForeignKey(Object_list_all, on_delete=models.CASCADE)
    Obs_date_current = models.DateField('观测日期', max_length=30)
    Obs_timewindow_begin = models.DateTimeField('可观测时间窗口起始时间', max_length=30)
    Obs_timewindow_end = models.DateTimeField('可观测时间窗口结束时间', max_length=30)
    Obs_complete_stage = models.CharField('观测完成状态', max_length=30, choices=STAGED_CHOICE)
    mode = models.CharField('模式', max_length=30, choices=MODE_CHOICE)

    class Meta:
        verbose_name = '待观测目标列表'
        verbose_name_plural = verbose_name
        db_table = 'Object_list_current'

    def __str__(self):
        return "%s" % self.Object_ID


#定义上传文件路径与名称
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    filetype = re.search(r'[^.]+\w$', filename).group()    #提取文件后缀名
    return os.path.join(filetype, filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True, verbose_name='文件')
    time = models.DateField(verbose_name='插入时间', auto_now_add=True)


#记录用户动作
class UserAction(models.Model):
    TYPE_CHOICE = (
        ('增加', '增加'),
        ('删除', '删除'),
        ('修改', '修改'),
    )
    username = models.CharField(verbose_name='用户名', max_length=30)
    action_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=True)
    action_type = models.CharField(verbose_name='修改类型', choices=TYPE_CHOICE, max_length=30)

    class Meta:
        verbose_name_plural = '用户动作'
        db_table = 'UserAction'