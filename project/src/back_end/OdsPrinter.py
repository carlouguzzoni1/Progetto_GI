from collections import OrderedDict
from pathlib import Path
from pyexcel_ods3 import save_data
from collections import OrderedDict
from project.src.back_end.AbstractPrinter import AbstractPrinter

class OdsPrinter(AbstractPrinter):
    """
    Classe utile per stampare i risultati in versione tabulata su
    file .ods.
    """

    def __new__(cls, *args, **kwargs):
        """
        Ovverride del metodo __new__ per creare una classe singleton: ogni
        volta che si vuole stampare su file .ods, si controlla se esiste già
        un'istanza della classe OdsPrinter. In tal caso, il metodo __new__ passa
        quell'istanza al metodo __init__
        """
        if not hasattr(cls, 'istance'):
            cls.istance = super(OdsPrinter, cls).__new__(cls)
        return cls.istance
    
    
    def __init__(self, retrieved, query="", sentiment=""):
        super().__init__(retrieved,query,sentiment)
        

    def formatOutput(self, nomefile):
        data = OrderedDict()
        temp = ([[value for value in row.values()]for row in self._retrieved])
        data.update({"Results": [[key for key in self._retrieved[0].keys()],*temp]})
        save_data(nomefile,data)        
        
