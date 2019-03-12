from django.forms import ModelForm
from django import forms
from.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class DataChangeForm(ModelForm):
    class Meta:
        model = Objects
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
        model = Objects
        exclude = ['Observer', 'Obs_stage']

    Observer = forms.IntegerField(label='观测者', widget=forms.widgets.Select())

    def __init__(self, *args, **kwargs):
        super(DataAddForm, self).__init__(*args, **kwargs)
        self.fields['Observer'].widget.choices = User.objects.values_list('id', 'username')


    # 检验观测目标是否重复
    def clean_Object_name(self):
        Object_name = self.cleaned_data['Object_name']
        if Objects.objects.filter(Object_name=Object_name).exists():
            raise forms.ValidationError('该观测目标已存在')
        return Object_name

    #检验经度格式是否正确
    def clean_Obj_RA(self):
        Obj_RA = self.cleaned_data['Obj_RA']
        value_dd = float(Obj_RA.split(":")[0]) + float(Obj_RA.split(":")[1]) / 60.0 + float(
            Obj_RA.split(":")[2]) / 3600.0
        return value_dd

    #检验纬度格式是否正确
    def clean_Obj_DEC(self):
        Obj_DEC = self.cleaned_data['Obj_DEC']
        value_dd = float(Obj_DEC.split(":")[0]) * 15.0 + float(Obj_DEC.split(":")[1]) / 60.0 * 15.0 + float(
            Obj_DEC.split(":")[2]) / 3600.0 * 15.0
        return value_dd


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