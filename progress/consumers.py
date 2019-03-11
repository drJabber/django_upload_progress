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

    #send task to free worker, set its state to 'busy'
    async def send_task_to_worker(self,task):
        await self.channel_layer.send('progress-worker',task)

    #each worker after made some part of work sends a 'progress' message here
    #message['id'] - progress value of workers task
    #message['progress'] - progress value of workers task
    #message['state'] - state of workers task: 'in progress', 'complete'
    async def worker_progress(self, message):
        print('progress:'+str(message['id'])+', progress='+str(message['progress']))
        await self.send(text_data=json.dumps(message))





# def worker(msg):
#     def delayed_message(reply_channel, progress, action):
#         return {
#             'channel': 'prog-rocker',
#             'content': {
#                 'reply_channel': reply_channel,
#                 'action': action,
#                 'progress': progress,
#             },
#             'delay': 200
#         }

#     async def delayed_send(msg):
#         await asyncio.sleep(200)
#         await Channel('prog-rocker').send(msg['content'], immediately=True)
#         # Channel('asgi.delay').send(msg, immediately=True)

#     def send_to_ws(reply_channel, content):
#         Channel(reply_channel).send({'text': json.dumps(content)})

#     def send_progress(reply_channel, progress):
#         send_to_ws(reply_channel, {'progress': progress})

#     action = msg.content['action']
#     reply = msg.content['reply_channel']

#     if action == 'start':
#         # start a long running background task!
#         # (this is just a mockup, using number to represent the progress of a background task)
#         progress = 0

#         send_progress(reply, progress)

#         new_msg = delayed_message(reply, progress, 'continue')
#         delayed_send(new_msg)

#     elif action == 'continue':
#         # check in on the background task
#         # (we are simulating a task by incrementing a number)
#         progress = msg.content['progress'] + 3
#         if progress >= 100:
#             send_to_ws(reply, {'complete': True, 'progress': 100})
#         else:
#             send_progress(reply, progress)
#             new_msg = delayed_message(reply, progress, 'continue')
#             delayed_send(new_msg)


# def ws_connect(msg):
#     msg.reply_channel.send({'text': json.dumps({"accept": True})})

# def ws_receive(message):
#     print(message)
#     data = json.loads(message['text'])
#     reply_channel = message.reply_channel.name

#     if data['action'] == 'start':
#         Channel('prog-rocker').send({
#             'reply_channel': reply_channel,
#             'action': 'start',
#         })


