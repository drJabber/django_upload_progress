import os
import mmap
from time import sleep
from .models import FileInfo, Node
from geopy.distance import distance
from django.contrib.gis.geos import Point,MultiPoint,GeometryCollection
from asgiref.sync import sync_to_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LineParser():

    async def parse(self, line, prevData):
        values = line.split("##")

        date = values[0].rstrip('\t').split('-')
        tag = date[0] + '-' + date[1] + '-' + date[2] + ' ' + date[3] + ':' + date[4] + ':' + date[5]

        values = values[1].split(";")

        data = {}
        for value in values:

            pair = value.split(":")

            if pair[0] == '4G':
                pair[0] = 'G4'

            if pair[0] == 'GPS':
                ll = pair[1].split(',')
                if (ll[1] != '0.000000') and (ll[2] != '0.000000'):
                    pair[1] = Point(float(ll[2]), float(ll[1]),srid=4326)
                    data['GPS'] = pair[1]    
                else:
                    return None, {}
            else:
                data[pair[0]] = pair[1].rstrip('\n')    

            sync_to_async(sleep(0))        

        if (prevData):
            dist=distance(prevData['GPS'], data['GPS'])
            data['dist']=prevData['dist']+abs(dist.m)
        else:
            data['dist']=0


        return tag, data

class Parser():
    async def linesCount(self,buffer):
        readline=buffer.readline
        lines=0
        while readline():
            lines+=1
            # sync_to_async(sleep(0.001))
        return lines    


    async def count_lines(self, message, channel_layer):
        reply_channel=message['reply-channel']
        filename=message['filename']
        fileid=message['id']

        dirName = os.path.join(BASE_DIR, 'info/')
        newDirName = os.path.join(BASE_DIR, 'info/old/')
        fullPath=os.path.join(dirName, filename)

        with open(fullPath,'r+b') as text:
            buffer=mmap.mmap(text.fileno(),0,prot=mmap.PROT_READ)

            lines=await self.linesCount(buffer)+1

            await channel_layer.send(reply_channel,{
                'type':'worker_prepared',
                'id':fileid,
                'lines': lines,
            })


    async def parse(self, message, channel_layer):
        reply_channel=message['reply-channel']
        filename=message['filename']
        fileid=message['id']
        
        dirName = os.path.join(BASE_DIR, 'info/')
        newDirName = os.path.join(BASE_DIR, 'info/old/')
        fullPath=os.path.join(dirName, filename)

        with open(fullPath,'r+b') as text:
            print(fullPath)
            buffer=mmap.mmap(text.fileno(),0,prot=mmap.PROT_READ)

            fileDate = filename.rstrip('.txt').split('-')
            date = fileDate[1] + '-' + fileDate[2] + '-' + fileDate[3] + ' ' + fileDate[4] + ':' + fileDate[5] 
            File = FileInfo.objects.create(name=filename, date=date)

            lineIdx=0

            lines=await self.linesCount(buffer)+1
            buffer.seek(0)
            print(lines)
            lineParser=LineParser()
            data=None
            for line in iter(buffer.readline,b""):
                tag, data =await lineParser.parse(line.decode('UTF8'),data) #returns DateTimeTag and dict of values
                lineIdx+=1

                if data:
                    row = Node.objects.create(dateTimeLabel=tag, fileInfo=File, **data)
                    if (lineIdx%100==0):
                        await channel_layer.send(reply_channel,{
                            'type':'worker_progress',
                            'id':fileid,
                            'progress': 100*lineIdx//lines,
                            'state' : 'incomplete'
                        })

            os.rename(dirName+filename, newDirName+filename)

            await channel_layer.send(reply_channel,{
                'type':'worker_progress',
                'id':fileid,
                'progress': 100,
                'state' : 'complete'
            })
