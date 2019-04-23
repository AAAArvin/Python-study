from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .models import *
import json
import random
import string


class HomeView(View):
    def get(self, request):
        return render(request, 'base.html', {})

    def post(self, request):
        if request.FILES:
            file = request.FILES.get("file")
            name = file.name
            size = int(file.size)
            with open('static/file/' + name, 'wb')as f:
                f.write(file.read())
            code = ''.join(random.sample(string.digits, 8))
            u = Upload(
                path='static/file/' + name,
                name=name,
                Filesize=size,
                code=code,
                PCIP=str(request.META['REMOTE_ADDR']),
            )
            u.save()
            return HttpResponsePermanentRedirect("/s/" + code)

class DisplayView(View):
    def get(self, request, code):
        uploads = Upload.objects.filter(code=str(code))
        if uploads:
            for upload in uploads:
                upload.DownloadDocount += 1
                upload.save()
        return render(request, 'content.html', {
            "content": uploads,
        })

class MyView(View):
    def get(self, request):
        IP = request.META['REMOTE_ADDR']
        uploads = Upload.objects.filter(PCIP=str(IP))
        for upload in uploads:
            upload.DownloadDocount += 1
            upload.save()
        return render(request, 'content.html', {
            "content": uploads,
        })

class SearchView(View):
    def get(self,request):
        code = request.GET.get("kw")
        uploads = Upload.objects.filter(name=str(code))
        data = {}
        if uploads :
            for i in range(len(uploads)):
                uploads[i].DownloadDocount +=1
                uploads[i].save()
                data[i]={}
                data[i]['download'] = uploads[i].DownloadDocount
                data[i]['filename'] = uploads[i].name
                data[i]['id'] = uploads[i].id
                data[i]['ip'] = str(uploads[i].PCIP)
                data[i]['size'] = uploads[i].Filesize
                data[i]['time'] = str(uploads[i].Datatime.strftime('%Y-%m-%d %H:%M:%S'))
                data[i]['key'] = uploads[i].code
        return HttpResponse(json.dumps(data), content_type="application/json")