from django.contrib.gis.geos import Point



class Parser():

    def parse(self, line):

        values = line.split("##")

        date = values[0].rstrip('\t').split('-')
        dateTimeTag = date[0] + '-' + date[1] + '-' + date[2] + ' ' + date[3] + ':' + date[4] + ':' + date[5]

        values = values[1].split(";")
        print(values)

        dictOfValues = {}
        for value in values:

            pair = value.split(":")

            if pair[0] == '4G':
                pair[0] = 'G4'

            if pair[0] == 'GPS':
                ll = pair[1].split(',')
                if (ll[1] != '0.000000') and (ll[2] != '0.000000'):
                    pair[1] = Point(float(ll[2]), float(ll[1]),srid=4326)
                    dictOfValues[pair[0]] = pair[1]    
                else:
                    return None, {}
            else:
                dictOfValues[pair[0]] = pair[1].rstrip('\n')    



        return dateTimeTag, dictOfValues

    
class Uploader():

    def upload(self, file, path):
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

