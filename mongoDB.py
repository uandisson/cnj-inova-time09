from pymongo import MongoClient
import csv
import pandas as pd

file = 'sgt_assuntos.csv'
file2 = 'sgt_classes.csv'


def banco():
    cliente = MongoClient('localhost', 27017)
    
    banco = cliente['processos-tjac']
    
    proc = banco['processos-tjac_2']
    
    p = proc.find()

    ass = assuntos()
    
    cla = classes()
    
    x = 0
    for a in p:
    
        try:
            cn = a['dadosBasicos']['assunto'][0]['codigoNacional']
            
            if not pesquisa(ass, cn):
                print(cn)
                print('False')
            
            cl = a['dadosBasicos']['classeProcessual']
    
            if not pesquisa(cla, cl):
                print(cn)
                print('False')
        
        except:
            a=0

        x +=1
    print(x)
    
def pesquisa(lista, chave):
    for r in lista:
        x=0
        t = r[x].split(';')[0]
        
        if str(t) == str(chave):
            return True
        
        x+=1
    return False

def assuntos():
    result = []
    with open(file) as assunto:
        reader = csv.reader(assunto)
        x = 0
        for row in reader:
            if True:
                result.append(row)
            x+=1

    return result

def classes():
    result = []
    with open(file2) as cl:
        reader = csv.reader(cl)
        x = 0
        for row in reader:
            if True:
                result.append(row)
            x+=1

    return result

if __name__ == "__main__":
    banco()    
