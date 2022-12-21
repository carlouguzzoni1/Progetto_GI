import csv
import time
import project.src.back_end.Tweet as tt
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
import random
import copy
from project.src.back_end.OdsPrinter import OdsPrinter
from project.src.back_end.CsvPrinter import CsvPrinter

class Database:
    """Classe che processa il file csv fornito come parametro al costruttore."""
    def __init__(self, csv_file):
        """
        Inizializza le strutture dati necessarie per la corretta costruzione del database.
        Scrive su file il nome del file .csv fornito.
        
        :param csv_file: ".csv" file
        """
        self.filename = csv_file
        self.reader = csv.reader(open(self.filename), delimiter = ",")
        self._tweets = [] # classi Tweet che contengono solo i fields di interesse
        self._fields = [] # contiene tutti i fields estratti dal file csv
        self._raw_data = [] # lista di dizionari, che corrispondono alle righe del file csv

        with open("csv_name.txt","w") as f:
            f.write(self.filename + "\n")
            
        
    def fillDb(self):
        """
        Metodo che riempie il database con i dati non processati. Costruisce una lista
        di dizionari, in cui ogni dizionario corrisponde ad una riga del file csv.
        """
        for count,row in enumerate(self.reader):
            if count == 0:
                self._fields = row
            else:
                dict = {}
                for i,field_text in enumerate(row):
                    dict[self._fields[i]] = field_text
                self._raw_data.append(dict)
                
    def filterFields(self, *args):
        """
        Metodo che filtra soltanto i campi del file csv di interesse, specificati come
        argomento. I dati grezzi vengono quindi processati e filtrati,
        per poi essere memorizzati in oggetti di classe Tweet.

        :param *args: list, lista di stringhe
        """
        for selected_field in args:
            if selected_field not in self._fields:
                raise Exception(selected_field + " non è presente tra i campi del file.")
        self._tweets.clear()
        for row in self._raw_data:
            filtered = dict(filter(lambda elem : (elem[0] in args), row.items()))
            t = tt.Tweet(filtered) 
#           t = tt.Tweet({key:value for (key,value) in row.items() if key in args}) 
            self._tweets.append(t)
           
    @property
    def tweets(self):
        return self._tweets
    
    @property
    def fields(self):
        return self._fields
    
    def __str__(self):
        """
        Stampa dei dati non processati.
        """
        return str(self._raw_data)
            
    def getSample(self, n, ods=False, csv=False):
        """
        Metodo per estrarre dai Tweet un campione casuale di n elementi.
        Aggiunge ad ogni tweet 10 parametri aggiuntivi (r1,r2...r10) che
        rappresentano ognuno il coefficiente di "rilevanza" per una query
        arbitraria (quindi per un totale di 10 query), scelta in fase
        di benchmarking. Sono inizialmente generati in modo casuale per
        ragioni didattiche. Si veda "calcolo del Distance Comulative Gain" per
        maggiori informazioni.
        :param n: integer, numerosità del campione casuale
        :param ods: boolean, stampa su file .ods
        :param csv: boolean, stampa su file .csv
        """
        sample = copy.deepcopy(random.sample(self.tweets, k=n))        
        for count in range(len(sample)):
            for q_index in range(10):
                exec("{}.r{}=random.randrange(4)".format("sample[count]",q_index+1))
        if ods == True:
            p = OdsPrinter([tweet.__dict__ for tweet in sample])
            p.formatOutput("sample.ods")

        if csv == True:
            cp = CsvPrinter([tweet.__dict__ for tweet in sample])
            cp.formatOutput("sample.csv")
