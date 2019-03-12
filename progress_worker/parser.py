import os
import mmap
from time import sleep
from .models import FileInfo, Node
from geopy.distance import distance
from django.contrib.gis.geos import Point,MultiPoint,GeometryCollection

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LineParser():

    async def parse(self, line, prevData):

        values = line.split("##")

        date = values[0].rstrip('\t').split('-')
        tag = date[0] + '-' + date[1] + '-' + date[2] + ' ' + date[3] + ':' + date[4] + ':' + date[5]

        values = values[1].split(";")
        print(values)

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

            await sleep(0)        

        dist=0
        if (prevData):
            dist=distance(prevData, data['GPS'])
            data['dist']=prevData['dist']+abs(dist)


        return tag, data

class Parser():
    async def linesCount(self,buffer):
        readline=buffer.readline
        lines=0
        while readline():
            lines+=1
            await sleep(0)
        return lines    


    async def parse(self, message, channel_layer):
        reply_channel=message['reply-channel']
        filename=message['filename']
        fileid=message['id']
        
        dirName = os.path.join(BASE_DIR, 'info/')
        newDirName = os.path.join(BASE_DIR, 'info/old/')
        fullPath=os.path.join(dirName, filename)

        with open(fullPath,'r+') as text:
            print(fullPath)
            buffer=mmap.mmap(text.fileno,0)

            fileDate = filename.rstrip('.txt').split('-')
            date = date[1] + '-' + date[2] + '-' + date[3] + ' ' + date[4] + ':' + date[5] 
            File = FileInfo.objects.create(name=filename, date=date)

            lineIdx=0

            lines=await self.linesCount(buffer)+1
            lineParser=LineParser()
            data=None
            for line in mmap:
                tag, data =await lineParser.parse(line,data) #returns DateTimeTag and dict of values
                lineIdx+=1

                if data:
                    row = Node.objects.create(dateTimeLabel=tag, fileInfo=File, **data)

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
