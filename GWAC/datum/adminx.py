import xadmin
from xadmin import views
from .models import *
from user.models import *

class AllModelAdmin(object):
    list_display = ['Object_name', 'Observer', 'Obj_RA', 'Obj_DEC', 'Obs_date_begin', 'Obs_date_end']
    search_fields = ['Object_name', 'Observer']
    list_filter = ['Obj_RA', 'Obj_DEC', 'Obs_date_begin', 'Obs_date_end']
    class Meta:
        model = Objects

class CurrentModelAdmin(object):
    list_display = ['Object_ID', 'Obs_date_current', 'Obs_timewindow_begin', 'Obs_timewindow_end', 'Obs_complete_stage', 'mode']
    class Meta:
        model = Object_list_current

xadmin.site.register(Objects, AllModelAdmin)
xadmin.site.register(Object_list_current, CurrentModelAdmin)

class ProfileInline(object):
    model = Profile
    can_delete = False


class UserAdmin(object):
    inlines = (ProfileInline, )
    list_display = ('username', 'is_superuser', 'user_level', 'company')

    def user_level(self, obj):
        return obj.profile.user_level
    user_level.short_description = '用户等级'
    def company(self, obj):
        return obj.profile.company
    company.short_description = '所属单位'

xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)


class ProfileAdmin(object):
    list_display = ('user', 'user_level', 'company', 'tel')
    class Meta:
        model = Profile

xadmin.site.register(Profile, ProfileAdmin)


class BaseSetting(object):
    enable_themes = 'True'
    use_bootswatch = 'True'

xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSettings(object):
    site_title="天文观测目标后台管理系统"
    site_footer="GWAC"
    menu_style="accordion"
xadmin.site.register(views.CommAdminView,GlobalSettings)

from xadmin import views
