import csv
import os


class DeliData:
    def __init__(self):
        print(os. getcwd())
        files = os.listdir('delidata_corpus')
        self.corpus = {}
        for f in files:
            if f == '__init__.py':
                continue
            with open('delidata_corpus/' + f, 'r', encoding="utf8") as rf:
                a = [{k: v for k, v in row.items()} for row in
                     csv.DictReader(rf, delimiter='\t', skipinitialspace=True)]
                self.corpus[f] = a



