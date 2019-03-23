# from channels import Cahnnel
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json
from time import sleep
from asgiref.sync import sync_to_async
import asyncio

class WSConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('try connect WS')
        self.tasks=[]
        self.prepared_tasks=[]
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
        if (data['type']=='collect'):
            await self.handle_collect_message(data['id'], data['filename'])
        elif (data['type']=='upload'):
            await self.handle_upload_message()

    async def handle_collect_message(self, id, filename):
        print('collect:',id, filename)
        self.tasks.append({
                'type':'upload_file', 
                'reply-channel':self.channel_name, 
                'id':id,
                'filename': filename,
            })

    async def handle_upload_message(self):
        print('start upload:')
        for future in asyncio.as_completed(map(lambda value:self.send_task_to_worker(
                {
                    'type':'prepare_file',
                    'reply-channel':value['reply-channel'],
                    'id':value['id'],
                    'filename':value['filename']
                }
            ),self.tasks)):
            await future


    async def send_task_to_worker(self,task):
        print('task: ',task['type'],' id=',task['id'])
        await self.channel_layer.send('progress-worker',task)   

    #each worker after made some part of work sends a 'progress' message here
    #message['id'] - progress value of workers task
    #message['progress'] - progress value of workers task
    #message['state'] - state of workers task: 'in progress', 'complete'
    async def worker_progress(self, message):
        if (message['state']=='complete'):
            print('task #',message['id'],' complete')
        await self.send(text_data=json.dumps(message))

    async def worker_prepared(self, message):
        id=message['id']
        lines=message['lines']
        task=list(filter(lambda x : x['id']==id,self.tasks))[0]
        task['lines']=lines
        self.prepared_tasks.append(task)
        print('prepared count=',len(self.prepared_tasks)  )      
        print('tasks count=',len(self.tasks) )       
        if (len(self.prepared_tasks)==len(self.tasks)):
            print('start parsing:')
            sorted_tasks=sorted(self.prepared_tasks, key=lambda k: k['lines'],reverse=False)

            for future in asyncio.as_completed(map(lambda value:self.send_task_to_worker(value),sorted_tasks)):
                await future
        












