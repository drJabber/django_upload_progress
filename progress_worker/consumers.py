from time import sleep
from channels.consumer import AsyncConsumer
import json
from random import randint,seed
from .parser import Parser

class BackgroundTaskConsumer(AsyncConsumer):
    async def upload_file(self, message):
        print('worker handle upload message')

        parser=Parser()
        await parser.parse(message,self.channel_layer)

    async def prepare_file(self, message):
        print('worker handle prepare message')

        parser=Parser()
        await parser.count_lines(message,self.channel_layer)
        



