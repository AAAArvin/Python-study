from django.db import models
import datetime

# Create your models here.

class Object_list_all(models.Model):
    '''
    观测目标列表总表
    '''
    STAGE_CHOICE = (
        ('0', 'current'),
        ('1', 'past'),
        ('2', 'future'),
        ('3', 'removed'),
    )

    MODE_CHOICE = (
        ('0', 'observation'),
        ('1', 'test'),
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
    Obs_stage = models.CharField('观测阶段', max_length=30, choices=STAGE_CHOICE)
    mode = models.CharField('模式', max_length=30, choices=MODE_CHOICE)

    class Meta:
        verbose_name = '观测目标列表总表'
        verbose_name_plural = verbose_name
        ordering = ['prioriy']

    def __str__(self):
        return "%s" % self.Object_name


class Object_list_current(models.Model):
    '''
    待观测目标列表
    '''
    STAGED_CHOICE = (
        ('0', 'scheduled'),
        ('1', 'completed'),
        ('2', 'canceled'),
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

    def __str__(self):
        return "%s" % self.Object_ID