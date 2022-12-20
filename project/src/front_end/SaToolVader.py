from project.src.front_end.SaTool import SaTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SaToolVader(SaTool):
    """
    Classe che implementa le funzionalità di sentiment analysis del tool
    Vader. Eredita dalla classe astratta SaTool.
    """

    def __init__(self):
        """
        Costruttore per l'analizzatore di Vader.
        """
        self._analyzer = SentimentIntensityAnalyzer()


    def compute_sentiment(self, text, sentiment):
        """
        Implementazione di metodo astratto per il calcolo del sentiment
        relativo ad un campo testuale.
        :param text:        str, campo testuale da analizzare.
        :param sentiment:   str, tipo di sentiment da valutare.
        """
        match sentiment:
            case "positive":
                return self._analyzer.polarity_scores(text)["pos"]
            case "negative":
                return self._analyzer.polarity_scores(text)["neg"]
            case "neutral":
                return self._analyzer.polarity_scores(text)["neu"]
            case "compound":
                return self._analyzer.polarity_scores(text)["compound"]

