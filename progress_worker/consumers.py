from time import sleep
from channels.consumer import AsyncConsumer
import json
from random import randint

class BackgroundTaskConsumer(AsyncConsumer):
    async def upload_file(self, message):

        print('handle upload message')
        await self.upload_long_long_file(message)


    async def upload_long_long_file(self, message):
        reply_channel=message['reply-channel']
        filename=message['filename']
        fileid=message['id']

        cnt=randint(1,20);
        for v in range(cnt):
            print('upload step: '+ str(v))
            await self.channel_layer.send(reply_channel,{
                'type':'worker_progress',
                'id':fileid,
                'progress': 100*v//cnt,
                'state' : 'incomplete'
            })
            sleep(1)

        await self.channel_layer.send(reply_channel,{
            'type':'worker_progress',
            'id':fileid,
            'progress': 100,
            'state' : 'complete'
        })





