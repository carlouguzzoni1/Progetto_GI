from project.src.front_end.SaTool import SaTool
from transformers import pipeline


class SaToolRoberta(SaTool):
    """
    Classe che implementa le funzionalità di sentiment analysis del tool
    Roberta. Eredita dalla classe astratta SaTool.
    """

    def __init__(self):
        """
        Costruttore per l'analizzatore di Roberta.
        """
        self._pipeline = pipeline(
            "text-classification",
            model = "j-hartmann/emotion-english-distilroberta-base",
            top_k = None
            )


    def compute_sentiment(self, text, sentiment):
        """
        Implementazione di metodo astratto per il calcolo del sentiment
        relativo ad un campo testuale.
        :param text:        str, campo testuale da analizzare.
        :param sentiment:   str, tipo di sentiment da valutare.
        """
        score = self._pipeline(text)
        # "Spacchetta" la struttura dati restituita da pipeline.
        scores = score[0]
        # Ordina alfabeticamente il dizionario dei risultati, per valore
        # di sentiment.
        scores = sorted(scores, key = lambda d : d["label"])

        match sentiment:
            case "anger":
                sent_score = scores[0]["score"]
            case "disgust":
                sent_score = scores[1]["score"]
            case "fear":
                sent_score = scores[2]["score"]
            case "joy":
                sent_score = scores[3]["score"]
            case "neutral":
                sent_score = scores[4]["score"]
            case "sadness":
                sent_score = scores[5]["score"]
            case "surprise":
                sent_score = scores[6]["score"]
