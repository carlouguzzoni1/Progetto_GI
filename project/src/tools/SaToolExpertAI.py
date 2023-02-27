from expertai.nlapi.cloud.client import ExpertAiClient
from project.src.tools.SaTool import SaTool
import os


"""
Versione della classe SaToolExpertAI in chiave singleton con decoratore.
Giustificazione: istanziare nuovi oggetti SaToolExpertAI sovrascrive le
variabili di ambiente EAI_USERNAME ed EAI_PASSWORD più volte, creando
confusione. Inoltre, essendo lo stesso tool deprecato ed in uso a soli
fini esplorativi, se ne vuole limitare il più possibile l'utilizzo.
L'utente dovrà quindi seguire la procedura di cancellazione riportata di
seguito, o riavviare il terminale, per istanziare nuovi oggetti SaToolExpertAI.

Creare l'oggetto:                   ai = SaToolExpertAI()
Cancellare la entry nella closure:  del Singleton.singleton.__globals__["SaTool\
                                    ExpertAI"].__closure__[1].cell_contents[type(ai)]
Cancellare del tutto l'oggetto:     del ai
"""


def singleton(cls):
    """
    Closure che mantiene le istanze delle classi passate come argomento
    in un dizionario, vanificando la creazione di nuovi oggetti SaToolExpertAI,
    ove viene applicata, a meno della cancellazione (operazione complicata).
    """
    instances = {}

    def getinstance(*args, **kwargs):
        """
        Se cls non esiste come chiave in instances, la inserisce come key,
        avente come value l'oggetto istanziato.
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return getinstance


@singleton
class SaToolExpertAI(SaTool):
    """
    Classe che implementa le funzionalità di sentiment analysis del tool
    ExpertAI. Eredita dalla classe astratta SaTool. Decorata con singleton.
    """

    def __init__(self, client = ExpertAiClient(), language = "en"):
        """
        Costruttore per l'analizzatore di expertAI.
        :param client:      ExpertAiClient, client che richiede i servizi
                            di ExpertAI.
        :param language:    str, linguaggio di riferimento per l'analisi.
        """
        print("Initializing ExpertAI client. Please, authenticate.")
        os.environ["EAI_USERNAME"] = input("Username: ")
        os.environ["EAI_PASSWORD"] = input("Password: ")
        self._client = client
        self._language = language


    # Di _client e _language si hanno solo i getter. Se si vuole modificare
    # radicalmente un oggetto ExpertAI, si rimanda alla creazione di uno
    # nuovo, avente le caratteristiche desiderate.
    @property
    def client(self):
        return self._client

    @property
    def language(self):
        return self._language


    def __del__(self):
        """
        Distruttore custom per l'analizzatore di expertAI. Se non vi sono
        istanze attive di ExpertAI, provvede all'eliminazione delle variabili
        d'ambiente del tool.
        """
        del os.environ["EAI_USERNAME"]
        del os.environ["EAI_PASSWORD"]


    def compute_sentiment(self, text, sentiment):
        """
        Implementazione di metodo astratto per il calcolo del sentiment
        relativo ad un campo testuale.
        :param text:        str, campo testuale da analizzare.
        :param sentiment:   str, tipo di sentiment da valutare.
        """
        output = self._client.specific_resource_analysis(
            body =   {"document": {"text": text}},
            params = {"language": self._language, "resource": "sentiment"}
            )

        if sentiment == "positive":
            return output.sentiment.positivity
        elif sentiment == "negative":
            return output.sentiment.negativity
        elif sentiment == "overall":
            return output.sentiment.overall
        
        # match sentiment:
        #     case "positive":
        #         return output.sentiment.positivity
        #     case "negative":
        #         return output.sentiment.negativity
        #     case "overall":
        #         return output.sentiment.overall
