import sys
from project.src.back_end.AbstractPrinter import AbstractPrinter
from functools import partial
from pathlib import Path
import sys


class TxtPrinter(AbstractPrinter):
    """
    Classe che implementa il metodo AbstractPrinter.formatOutput() per stampare
    i risultati su file testuale o su stdout.
    """
    
    def __new__(cls, *args, **kwargs):
        """
        Ovverride del metodo __new__ per creare una classe singleton: ogni
        volta che si vuole stampare su file .txt, si controlla se esiste già
        un'istanza della classe TxtPrinter. In tal caso, il metodo __new__ passa
        quell'istanza al metodo __init__
        """
        if not hasattr(cls, 'istance'):
            cls.istance = super(TxtPrinter, cls).__new__(cls)
        return cls.istance


    def __init__(self, retrieved, query="", sentiment=""):
        """
        Legge i file "frame.txt", "separator.txt" e "title.txt", contenenti 
        delle "cornici" per avere una stampa leggibile.
        :param searcher: Searcher
        :param results: Results
        """
        super().__init__(retrieved, query, sentiment)
        f = Path(__file__).with_name("./frame.txt")
        s = Path(__file__).with_name("./separator.txt")
        t = Path(__file__).with_name("./title.txt")
        
        with open(f.absolute(), "r") as frame, open(s.absolute(), "r") as separator, open(t.absolute(), "r") as title:
            self.frame = frame.read()
            self.separator = separator.read()
            self.title = title.read()
        
        # with open('./frame.txt', 'r') as frame, open('./separator.txt', 'r') as sep, open('./title.txt', 'r') as title:
        #     self.frame = frame.read()
        #     self.separator = sep.read()
        #     self.title = title.read()
        
    def formatOutput(self,nomefile=sys.stdout):
        """
        Metodo che stampa i risultati formattati.
        """
        file_obj = None
        if nomefile != sys.stdout:
            file_obj = open(nomefile, "w")

        pprint = partial(print, file=file_obj)    
        pprint(self.title)
        pprint(self.frame, end='')
        pprint(
            "Query: ", self.raw_query,
            "\nNumero di risultati: ", len(self._retrieved),
            "\nSentiment: ", self.sentiment,
        )
        pprint(self.frame)
        for element in self._retrieved:
            for key, value in element.items():
                pprint(key + " --> " + str(value))
            pprint(self.separator)
        if(file_obj):
            file_obj.close()


