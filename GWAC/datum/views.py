# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datum import forms
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, HttpResponseRedirect



#展示所有观测数据
def index(request):
    lists = Object_list_all.objects.all()
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
    context = {}
    context['lists'] = lists
    context['page_of_lists'] = lists_all
    context['page_range'] = page_range
    context['lists_current'] = Object_list_current.objects.all()
    context['list_form'] = forms.DataAddForm()
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
        data.Obs_stage = 'removed'
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

#上传文件
@login_required(login_url='/accounts/login')
def upload_file(request):
    pass