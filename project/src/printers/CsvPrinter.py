from pathlib import Path
from project.src.printers.AbstractPrinter import AbstractPrinter
import csv

class CsvPrinter(AbstractPrinter):
    """
    Classe utile per stampare i risultati in formato .csv.   
    """
    def __new__(cls, *args, **kwargs):
        """
        Ovverride del metodo __new__ per creare una classe singleton: ogni
        volta che si vuole stampare su file .csv, si controlla se esiste già
        un'istanza della classe CsvPrinter. In tal caso, il metodo __new__ passa
        quell'istanza al metodo __init__
        """
        if not hasattr(cls, 'istance'):
            cls.istance = super(CsvPrinter, cls).__new__(cls)
        return cls.istance
    
    def __init__(self, retrieved, query="", sentiment=""):
        super().__init__(retrieved,query,sentiment)
        
    def formatOutput(self,nomefile):

        header = [key for key in self._retrieved[0].keys()]
        data = [[value for value in tweet.values()] for tweet in self._retrieved]

        with open(nomefile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
        
            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(data)
