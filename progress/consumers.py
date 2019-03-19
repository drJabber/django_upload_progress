# from channels import Cahnnel
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json

class WSConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('try connect WS')
        await self.accept()


    async def disconnect(self, code ):
        print('try disconnect')

    #receives command from WS
    # //upload message:
    # //'id' - file id
    # //'filename' - uploaded file name
    # //'type' = upload command
    async def receive(self, text_data=None, bytes_data=None):
        print('try receive:')
        print(text_data)
        data=json.loads(text_data)
        await self.send_task_to_worker(
            {
                'type':'upload_file', 
                'reply-channel':self.channel_name, 
                'id':data['id'],
                'filename': data['filename'],
            }
        )

    async def send_task_to_worker(self,task):
        await self.channel_layer.send('progress-worker',task)

    #each worker after made some part of work sends a 'progress' message here
    #message['id'] - progress value of workers task
    #message['progress'] - progress value of workers task
    #message['state'] - state of workers task: 'in progress', 'complete'
    async def worker_progress(self, message):
        print('progress:'+str(message['id'])+', progress='+str(message['progress']))
        await self.send(text_data=json.dumps(message))
