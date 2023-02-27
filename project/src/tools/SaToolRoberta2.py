from project.src.tools.SaTool import SaTool
from transformers import pipeline


class SaToolRoberta2(SaTool):
    """
    Classe che implementa le funzionalità di sentiment analysis del tool
    Roberta. Eredita dalla classe astratta SaTool.
    """

    def __init__(self):
        """
        Costruttore per l'analizzatore di Roberta.
        """
        self.classifier = pipeline("sentiment-analysis",top_k = None)



    def compute_sentiment(self, text, sentiment):
        """
        Implementazione di metodo astratto per il calcolo del sentiment
        relativo ad un campo testuale.
        :param text:        str, campo testuale da analizzare.
        :param sentiment:   str, tipo di sentiment da valutare.
        """
        score = self.classifier(text)
        if sentiment == "positive":
            print(score[0][0]["score"])
            return score[0][0]["score"]
        elif sentiment == "negative":
            return score[0][1]["score"]

