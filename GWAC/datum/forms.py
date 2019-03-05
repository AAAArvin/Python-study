from django.forms import ModelForm
from django import forms
from.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class DataChangeForm(ModelForm):
    class Meta:
        model = Object_list_all
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DataChangeForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({
                'class': 'form-control'
            })


class DataAddForm(ModelForm):
    #增加一条观测目标表单
    class Meta:
        model = Object_list_all
        fields = '__all__'

    # 检验观测者是否存在
    def clean_Observer(self):
        Observer = self.cleaned_data['Observer']
        if not User.objects.filter(username=Observer).exists():
            raise forms.ValidationError('该用户不存在')
        return Observer

    # 检验观测目标是否重复
    def clean_Object_name(self):
        Object_name = self.cleaned_data['Object_name']
        if Object_list_all.objects.filter(Object_name=Object_name).exists():
            raise forms.ValidationError('该观测目标已存在')
        return Object_name

    '''#检验经度格式是否正确
    def clean_Obj_RA(self):
        Obj_RA = self.cleaned_data['Obj_RA']

    #检验纬度格式是否正确
    def clean_Obj_DEC(self):
        Obj_DEC = self.cleaned_data['Obj_DEC']'''


class FileUploadModelForm(ModelForm):
    class Meta:
        model = File
        fields = '__all__'
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'file',
            }),
        }


class UserActionForm(ModelForm):
    class Meta:
        model = UserAction
        fields = '__all__'