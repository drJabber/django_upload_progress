    
class Uploader():

    def upload(self, file, path):
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

