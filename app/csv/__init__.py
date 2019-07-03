import csv


class Xcsv(object):
    def __init__(self, license):
        self.filename = "output/%s.xcsv" % license

    def loadCsv(self):
        lists = []
        with open(self.filename, mode='r') as csv_file:
            data = csv.DictReader(csv_file)
            for line in data:
                lists.append(line['repositorio'].split('/'))
        return lists
