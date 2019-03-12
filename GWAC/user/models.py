from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    LEVEL_CHOICE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户名')
    user_level = models.CharField('用户等级', choices=LEVEL_CHOICE, max_length=30)
    company = models.CharField('所属单位', max_length=30, default='')
    tel = models.CharField('电话', max_length=30, default='')

    def __str__(self):
        return '<Profile: %s, %s, %s, %s>' % (self.user_level, self.user.username, self.company, self.tel)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

def get_user_level(self):
    profile = Profile.objects.get(user=self)
    return profile.user_level

def get_company(self):
    profile = Profile.objects.get(user=self)
    return profile.company

def get_tel(self):
    profile = Profile.objects.get(user=self)
    return profile.tel

User.get_user_level = get_user_level
User.get_company = get_company
User.get_tel = get_tel