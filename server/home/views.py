from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import UploadedFiles 
from . import forms
import os
import subprocess
from django.core.serializers import serialize

# Create your views here.
dir_name = os.getcwd()+'/home'
def home(request):
    # print(request)
    response = JsonResponse(serialize('json',UploadedFiles.objects.all()),safe=False)
    response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
    return response
def JSFiles(request,file):
    if(file.find('shakaplayer')!= -1 or file.find('shaka-player')!= -1):
        with open('/home/seth/shaka-player/dist/shaka-player.compiled.debug.js','r') as jsfile:
            return HttpResponse(jsfile.read(),content_type='text/javascript')
    else:
        with open(dir_name+'/node_modules/hls.js/dist/{filename}'.format(filename=file),'r') as jsfile:
            return HttpResponse(jsfile.read(),content_type='text/javascript')

def httpResponse(message):
    response = HttpResponse(message)
    response["Access-Control-Allow-Origin"] = 'http://localhost:3000/'
    return response

def fileSource(request, src):
    try:
        if(src.endswith('.mp4') or src.endswith('.jpg')):
            
            with open(dir_name+'/files/{src}'.format(src=src),'rb')  as file:
                response = HttpResponse(file.read())
                if src.endswith('.jpg'):
                    response['Content-Type'] = 'image/jpeg'
                response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
                response["Access-Control-Allow-Headers"] = '*' 
                return response
        else:
            with open(dir_name+'/files/{src}'.format(src=src),'r')  as file:
                response = HttpResponse(file.read())
                response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
                return response
    except:
        response = HttpResponse('filesource error')
        response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
        return response

def fileSourceFormat(request, src,src1):
    try: 
        with open(dir_name+'/files/{src}/{src1}'.format(src=src,src1=src1),'rb') as file:
            response = HttpResponse(file.read())
            response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
            return response 
    except:
        response = HttpResponse("error")
        response["Access-Control-Allow-Origin"] = 'http://localhost:3000'
        return response
def createHLS(request):
    if request.method == 'POST':
        def handle_uploaded_file(f):
            media_dir = dir_name + '/files/'
            try:
                with open(dir_name+'/files/{filename}'.format(filename=request.FILES["file"]), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            except IsADirectoryError:
                pass
            except:
                httpResponse('error')
            def fileFormat(size):
                if size == "poster":
                    original = media_dir+'{size}'.format(size=size)+str(request.FILES['file'])+'.jpg'
                    return original
                else:
                    original = media_dir+'{size}'.format(size=size)+str(request.FILES['file'])+'.mp4'
                    return original
            ffmpeg = subprocess.run(['ffmpeg','-t', '59',
            '-i', '%s'% (media_dir+str(request.FILES['file'])),'-s',' 720x360',fileFormat('720'),
            '-i', '%s'% (media_dir+str(request.FILES['file'])),'-r',' 1','-frames','1','-ss','30',fileFormat('poster'),
            '-i', '%s'% (media_dir+str(request.FILES['file'])),'-s',' 640x480',fileFormat('480'),
            '-y'])

            if ffmpeg.returncode == 0:
                os.remove(media_dir+str(request.FILES['file']))
                if request.POST['type']=='DASH':
                    shaka = subprocess.run(["packager","in={audio},stream=audio,output={audiooutput}.mp4".format(audio=fileFormat('720'),audiooutput=fileFormat('720')),
                    "in={original},stream=video,output={videooutput}".format(original=fileFormat('720'),videooutput=fileFormat('shaka720')),
                    "in={original},stream=video,output={videooutput}".format(original=fileFormat('480'),videooutput=fileFormat('shaka480')),
                     "--mpd_output", "{mpd}.mpd".format(mpd=media_dir+str(request.FILES['file']))])
                    if shaka.returncode == 0:
                        UploadedFiles.objects.create(name=request.POST['name'],streamType='HLS',url=str(request.FILES['file'])+'.mpd',poster='poster%s.jpg'%str(request.FILES['file']))
                        return httpResponse('done')
                    else:
                        return httpResponse('error')
                elif request.POST['type']=='HLS':
                    shaka = subprocess.run(["packager",
                    "in={audio},stream=audio,segment_template=./home/files/{audiooutput}aac/$Number$.aac,playlist_name={audiooutput}aac/main.m3u8,hls_group_id=audio,hls_name=ENGLISH".format(audio=fileFormat('720'),audiooutput=str(request.FILES['file'])), 
                    "in={original},stream=video,segment_template=./home/files/{videooutput}ts/$Number$.ts,playlist_name={videooutput}ts/main.m3u8,iframe_playlist_name={videooutput}ts/iframe.m3u8".format(original=fileFormat('720'),videooutput=str(request.FILES['file'])), 
                    "in={original},stream=video,segment_template=./home/files/{videooutput}ts/$Number$.ts,playlist_name={videooutput}ts/main.m3u8,iframe_playlist_name={videooutput}ts/iframe.m3u8".format(original=fileFormat('480'),videooutput=str(request.FILES['file'])), 
                     "--hls_master_playlist_output", "./home/files/{m3u8}.m3u8".format(m3u8=str(request.FILES['file']))])
                    if shaka.returncode == 0:
                        UploadedFiles.objects.create(name=request.POST['name'],streamType='HLS',url=str(request.FILES['file'])+'ts/main.m3u8',poster='poster%s.jpg'%str(request.FILES['file']))
                        return httpResponse('done')
                    else:
                        return httpResponse('error')
                return httpResponse('done')
            else:
                return httpResponse('error')
        return handle_uploaded_file(request.FILES['file'])
        
    else:
        return HttpResponse('error')
