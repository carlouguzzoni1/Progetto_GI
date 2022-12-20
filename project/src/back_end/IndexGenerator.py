import sys
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
import os, os.path
from tqdm import tqdm

class IndexGenerator:
    """
    Classe che crea l'indice con cui si interfacceranno
    le query di ricerca. L'utente deve fornire in input lo schema
    da lui desiderato, insieme ad un'oggetto di classe Database contenente
    i tweet ottenuti dal file csv.
    """
    def __init__(self, schema, database):
        """
        Crea e predispone la cartella in cui verranno memorizzati i dati
        relativi all'indice.
        :param schema: Schema, definito dall'utente
        :param database: Database, contiene i tweets estratti dal file csv
        """
        self.index_dir = "./Index/"
        self.schema = schema
        self.database = database
        
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)            
        ix = index.create_in(self.index_dir, self.schema)
        ix = index.open_dir(self.index_dir)
        
        self.writer = ix.writer()
        
    def fillIndex(self):
        """
        Metodo che riempie l'indice con i Tweets contenuti nel database.
        In base alla grandezza del database, questo metodo potrebbe richiedere
        più tempo.
        """
        print("Filling Index with Tweets, fields are:")
        for name in self.schema._subfields.keys():
            print("> " + name)
        field_names = self.schema._subfields        
        for tweet in tqdm(self.database.tweets):                        
            self.writer.add_document(**{field_name:tweet.__dict__[field_name] for field_name in field_names})
        print("Committing files...")
        self.writer.commit()
