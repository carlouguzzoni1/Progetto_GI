import sys
from abc import ABC, abstractmethod

class AbstractPrinter:
    """
    Classe astratta, da cui ereditano le classi TxtPrinter e OdsPrinter. 
    Le classi che ereditano da questa classe astratta devono implementare
    il metodo "formatOutput".    
    """
    
    def __init__(self, retrieved, query="", sentiment=""):
        """
        :param retrieved: lista di dizionari, oggetto della stampa
        :param query: string, query da cui sono stati estratti i risultati (default = "")
        :param sentiment: string, sentimento sulla base del quale è stato fatto il ranking (default = "")
        """
        self._raw_query = query
        self._sentiment = sentiment
        self._retrieved = retrieved
        
    @abstractmethod
    def formatOutput(self, nomefile):
        """
        Metodo che devono implementare le classi che ereditano da questa
        classe astratta. Deve eseguire le operazioni necessarie per stampare
        i risultati su un file del formato appropriato.
        :param nomefile: string
        """
        pass

    @property
    def raw_query(self):
        return self._raw_query

    @property
    def sentiment(self):
        return self._sentiment

    @property
    def retrieved(self):
        return self._retrieved
    
    
    def __str__(self):
        """
        Overload del metodo __str__. Stampa i risultati senza formattazione,
        utile in caso di debugging. Stampa un warning in caso di "wall of text".
        """
        val = self.raw_query + "\n"
        if len(self.retrieved) > 100:
            a = int(input("Warning: output consists of more than 100 tweets. Press 1 for non-verbose output, 2 otherwise.\n >> "))
            if a == 2:
                return str(self.retrieved)
            elif a == 1:
                return str([self.retrieved[i] for i in range(100)])
            else:
                raise ValueError
