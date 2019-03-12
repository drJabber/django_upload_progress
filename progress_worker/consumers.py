from time import sleep
from channels.consumer import AsyncConsumer
import json
from random import randint
from parser import Parser

class BackgroundTaskConsumer(AsyncConsumer):
    async def upload_file(self, message):

        print('handle upload message')
        parser=Parser()

        await parser.parse(message)


