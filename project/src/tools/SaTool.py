from abc import ABC, abstractmethod


class SaTool(ABC):
    """
    Classe astratta per tool di sentiment analysis.
    """

    @abstractmethod
    def compute_sentiment(self, text, sentiment):
        """
        Metodo astratto per il calcolo del sentiment relativo ad un campo
        testuale.
        :param text:        str, campo testuale da analizzare.
        :param sentiment:   str, tipo di sentiment da valutare.
        """
        pass
