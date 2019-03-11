from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.gis.db.models import Extent, GeometryField,PointField
from django.contrib.gis.geos import Point,MultiPoint,GeometryCollection
from django.contrib.gis.measure import D


import os
from geopy.distance import distance

from .additionals import Parser, Uploader
from progress_worker.models import FileInfo, Node
from .forms import UploadForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(request):
    return render(request, 'main.html')

def testPars(request):
    
    dirName = os.path.join(BASE_DIR, 'info/')
    newDirName = os.path.join(BASE_DIR, 'info/old/')
    # filesList = os.listdir(dirName)
    filesList = (file for file in os.listdir(dirName) 
        if os.path.isfile(os.path.join(dirName, file)))

    files=[]
    for file in filesList:
        files.append({'name':file,'index':len(files)})

    return render(request,'parse.html',{'files':files})

        # with open(os.path.join(dirName, file)) as text:

        #     date = file.rstrip('.txt').split('-')
        #     date = date[1] + '-' + date[2] + '-' + date[3] + ' ' + date[4] + ':' + date[5] 
        #     File = FileInfo.objects.create(name=file, date=date)

        #     cnt=0
        #     dist=0 
        #     d=0
        #     for line in text:
        #         parser = Parser()
        #         tag, data = parser.parse(line) #returns DateTimeTag and dict of values
        #         if data:
        #             cnt+=1
        #             if cnt == 1:
        #                 d = distance(data['GPS'], data['GPS'])
        #                 dist = d.m
        #                 data['dist'] = dist
        #                 prevp = data['GPS']
        #                 # print(dist)
        #             else:
        #                 d = distance(prevp, data['GPS'])
        #                 dist+= d.m
        #                 data['dist'] = dist
        #                 prevp = data['GPS']
        #                 print(d.m)
        #                 print(dist)

        #         if data:
        #             row = Node.objects.create(dateTimeLabel=tag, fileInfo=File, **data)
            
        #     os.rename(dirName+file, newDirName+file)

    # return HttpResponse('Done')


def uploadFile(request):

    if request.method == 'POST':

        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            if  FileInfo.objects.filter(name=request.FILES['file'].name).exists():
                return HttpResponse('File already in DB')

            else:
                uploader = Uploader()
                path = os.path.join(BASE_DIR, 'info/') + request.FILES['file'].name
                uploader.upload(request.FILES['file'], path)
                return HttpResponse('Good')

    else:

        form = UploadForm()

    return render(request, 'upload.html', {'form': form})



def listFiles(request):
    filesList = FileInfo.objects.all()
    paginator = Paginator(filesList, 5) 
    print(filesList)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    return render(request, 'list.html', {'files': files})


def hello(request):
    return render(request, 'start.html')
