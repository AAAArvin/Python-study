# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datum import forms
import datetime
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, HttpResponseRedirect



#展示所有观测数据
def index(request):
    lists = Object_list_all.objects.all()
    list_total = Object_list_all.objects.filter(Obs_stage__in=['current', 'past', 'future'])

    #记录今天插入观测目标数量
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    lists_today_insert = Object_list_all.objects.filter(insert_time__year=year, insert_time__month=month, insert_time__day=day, Obs_stage__in=['current', 'past', 'future'])

    #根据当前时间，判断观测目标的观测阶段
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    past_lists = Object_list_all.objects.filter(Obs_date_end__lt=now, Obs_stage__in=['current', 'past', 'future'])
    for past_list in past_lists:
        past_list.Obs_stage = 'past'
        past_list.save()
    future_lists = Object_list_all.objects.filter(Obs_date_begin__gt=now, Obs_stage__in=['current', 'past', 'future'])
    for future_list in future_lists:
        future_list.Obs_stage = 'future'
        future_list.save()
    current_lists = Object_list_all.objects.filter(Obs_date_begin__lte=now, Obs_date_end__gte=now, Obs_stage__in=['current', 'past', 'future'])
    for current_list in current_lists:
        current_list.Obs_stage = 'current'
        current_list.save()

    #分页
    paginator = Paginator(lists, settings.EACH_PAGE_DATA_NUMBER)
    page_num = request.GET.get('page', 1)
    lists_all = paginator.get_page(page_num)
    current_page_num = lists_all.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #文件上传
    if request.method == "POST":
        form = forms.FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = forms.FileUploadModelForm()

    context = {}
    context['lists'] = lists
    context['list_total'] = list_total
    context['lists_today_insert'] = lists_today_insert
    context['page_of_lists'] = lists_all
    context['page_range'] = page_range
    context['lists_current'] = Object_list_current.objects.all()
    context['list_form'] = forms.DataAddForm()
    context['form'] = form
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login')
#观测数据以表单形式在前端展示
def detail(request, data_pk):
    context = {}
    data = get_object_or_404(Object_list_all, pk=data_pk)
    if request.method == 'POST':
        #后端数据填充到表单，同时后台表单接受前端修改的数据
        form = forms.DataChangeForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            #返回修改前页面
            return redirect(request.path)
    else:
        form = forms.DataChangeForm(instance=data)
    context['data'] = form
    return render(request, 'detail.html', context)


@login_required(login_url='/accounts/login')
#删除勾选的观测数据
def delete_datum(request):
    check_box_list = request.POST.getlist('check-box')
    for id in check_box_list:
        data = Object_list_all.objects.get(id=id)
        data.Obs_stage = 'remove'
        data.save()
        #还需要记录每次修改数据的用户以及时间
    return render(request, 'index.html')


@login_required(login_url='/accounts/login')
def data_add_form(request):
    data_form = forms.DataAddForm(request.POST)
    data = {}
    if data_form.is_valid():
        #向数据库写入观测数据
        data_form.save()
        data['status'] = 'SUCCESS'
    else:
        data['status'] = list(data_form.errors.values())[0][0]
    # 还需要记录每次修改数据的用户以及时间
    return JsonResponse(data)


#下载文件
@login_required(login_url='/accounts/login')
def download_data_csv(request):
    pass


#管理文件
@login_required(login_url='/accounts/login')
def file_manage(request):
    files = File.objects.all().order_by('-id')
    return render(request, 'file.html', {
        'files': files,
    })


#批量从文件从导入数据
def import_data_from_files(request, file_time, file_pk):
    import_file = get_object_or_404(File, id=file_pk)
    #提取文件后缀名
    filetype = re.search(r'[^.]+\w$', import_file.file.name).group().lower()
    context = {}
    context['status'] = 100    # 文件处理状态，101表示文件类型无法处理
    if filetype == 'txt':
        # 处理txt文件
        for line in open(import_file.file.name):
            pass
    elif filetype == 'csv':
        #处理csv文件
        pass
    elif filetype == 'xls' or filetype == 'xlsx':
        pass
    elif filetype == 'doc' or filetype == 'docx':
        pass
    else:
        context['status'] = 101
    return HttpResponse(filetype)


#搜索观测目标
def search(request):
    q = request.GET.get('q')
    context = {}
    '''results_lists = Object_list_all.objects.filter(
        # 筛选条件，可添加或移除
        Q(Object_name__icontains=q) |
        Q(Object_alias_1__icontains=q) |
        Q(Object_alias_2__icontains=q) |
        Q(Obj_Type__icontains=q) |
        Q(Obj_source__icontains=q) |
        Q(Observer__icontains=q) |
        Q(Obs_program__icontains=q) |
        Q(Group_ID__icontains=q) |
        Q(Unit_ID__icontains=q) |
        Q(Observation_type__icontains=q) |
        Q(Observation_strategy__icontains=q) |
        Q(note__icontains=q) |
        Q(Obs_stage__icontains=q) |
        Q(mode__icontains=q)
    )'''
    print(q)
    results_lists = Object_list_all.objects.filter(Object_name=q)
    context['results'] = results_lists
    return render(request, 'results.html', context)