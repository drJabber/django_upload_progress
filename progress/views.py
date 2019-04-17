from django.shortcuts import render,redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator
from django.contrib.gis.db.models import Extent, GeometryField,PointField
from django.contrib.gis.geos import Point,MultiPoint,GeometryCollection
from django.contrib.gis.measure import D


import os
from geopy.distance import distance

from .additionals import Uploader
from progress_worker.models import FileInfo, Node
from .forms import UploadForm
from PIL import Image


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


def uploadFile(request):

    if request.method == 'POST':

        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            if  FileInfo.objects.filter(name=request.FILES['file'].name).exists():
                request.session['result_msg']='Upload failed - file already in DB'
                return redirect(request.path_info)
            else:
                uploader = Uploader()
                path = os.path.join(BASE_DIR, 'info/') + request.FILES['file'].name
                uploader.upload(request.FILES['file'], path)
                request.session['result_msg']='Upload Ok'
                return redirect(request.path_info)

    else:

        form = UploadForm()
    print(request.session.get('result_msg','Empty msg'))
    return render(request, 'upload.html', {'form': form, 'result_msg': request.session.get('result_msg','')})



def listFiles(request):
    filesList = FileInfo.objects.all()
    paginator = Paginator(filesList, 5) 
    print(filesList)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    return render(request, 'list.html', {'files': files})


def hello(request):
    return render(request, 'start.html')


def loadPicture(request):
    path = os.path.join(BASE_DIR, 'info/')+'404.png'
    img=Image.open(path)

    alpha = Image.new('L', img.size, 128)
    img.putalpha(alpha)


    response=HttpResponse(content_type='application/octet-stream')
    
    img.save(response,"png")
    return response