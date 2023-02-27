from project.src.tools.SaToolFactory import SaToolFactory
from project.src.printers.AbstractPrinter import AbstractPrinter
from project.src.printers.TxtPrinter import TxtPrinter
from project.src.printers.OdsPrinter import OdsPrinter
from project.src.printers.CsvPrinter import CsvPrinter
from pathlib import Path
import sys


class Results:
    """
    Classe che costruisce la struttura dati dei risultati di una query,
    incrociando il punteggio di pertinenza con quello del sentiment.
    Fornisce funzioni per il cambiamento di sentiment e tool di sentiment
    analysis impostati, e funzioni di stampa.
    """


    def __init__(self, tool_name, sentiment, results, textual_field = "text",
                 ranking_fun = "balanced_weighted_avg"):
        """
        Costruttore di classe.
        :param tool_name:       str, nome del tool di sentiment analysis.
        :param sentiment:       str, tipo di sentiment da considerare.
        :param results:         Results, oggetto generato da una query su un
                                indice Whoosh.
        :param textual_field:   str, "text" di default, nome campo testuale su
                                cui fare sentiment analysis.
        :param ranking_fun:     str, "naive" di default, nome associato alla
                                funzione di ranking da usare.
        """
        # Selezione del tool per sentiment analysis.
        self.__select_tool(tool_name)
        # Selezione del sentiment.
        self._sentiment = SaToolFactory.check_sentiment(tool_name, sentiment)
        # Elaborazione risultati.
        self.__elaborate_results(results, textual_field)
        # Ordinamento risultati.
        self.__order_results(ranking_fun)


    # Rende disponibile il tool di sentiment analysis anche al di fuori
    # dell'oggetto istanziato.
    @property
    def sa_tool(self):
        return self._sa_tool

    # Il tool di sentiment analysis può essere stampato e cambiato attraverso
    # i getter/setter.
    @property
    def sa_tool_name(self):
        return self._sa_tool_name

    @sa_tool_name.setter
    def sa_tool_name(self, value):
        self.__select_tool(value)

    # Il sentiment è leggibile e modificabile attraverso i getter/setter.
    @property
    def sentiment(self):
        return self._sentiment

    @sentiment.setter
    def sentiment(self, value):
        # Si usa il metodo statico di SaToolFactory per valutare la correttezza.
        self._sentiment = SaToolFactory.check_sentiment(
            self._sa_tool_name,
            value
            )
    
    # Getter per la struttura dati dei risultati ordinati.
    @property
    def ordered(self):
        return self._ordered
    
    
    def __select_tool(self, tool_name):
        """
        Seleziona un tool per sentiment analysis e lo imposta come attributo
        di istanza.
        :param tool_name:   str, nome del tool per sentiment analysis.
        """
        # Tenta di costruire dinamicamente l'oggetto appropriato, usando
        # come interfaccia la classe Factory.
        try:
            tool = eval("SaToolFactory.make_{}()".format(tool_name))
        except:
            raise ValueError("Wrong tool name.")

        # Imposta tool e nome del tool come attributi di istanza.
        self._sa_tool = tool
        self._sa_tool_name = tool_name


    def __elaborate_results(self, results, textual_field):
        """
        Costruisce la struttura dati dei risultati, partendo dal prodotto
        di una query sull'indice. In particolare, la struttura dati in
        questione è una lista di dizionari.
        Applica il tool di sentiment analysis per il calcolo del relativo
        valore.
        """
        # Lancia Exception se non sono presenti risultati.
        if not results:
            raise Exception("No result for this query.")

        self._ordered = []
        # Sequenza di costruzione di _ordered.
        for hit in results:
            result = dict()
            # Aggiunge il numero d'indice del documento.
            result["docnum"] = hit.docnum
            # Aggiunge tutti i campi indicizzati del documento.
            result.update(dict(hit))
            # Aggiunge lo score di pertinenza del documento.
            result["pert_score"] = hit.score
            # Aggiunge il sentiment score del documento valutando il campo
            # testuale principale.
            result["sent_score"] = self._sa_tool.compute_sentiment(
                hit[textual_field],
                self._sentiment
                )
            self._ordered.append(result)


    def __order_results(self, ranking_fun):
        """
        Ordina la struttura dati dei risultati in base ad una formula di
        ordinamento predefinita, che combina il punteggio di pertinenza con
        quello relativo al sentiment.
        """
        # Determina la funzione di ranking in base al parametro.
        if ranking_fun == "naive":
            def ranking_calc(a, b):
                return a * b
        elif ranking_fun == "weighted_avg":
            def ranking_calc(a, b, wa = 0.6, wb = 0.4):
                return a * wa + b * wb
        elif ranking_fun == "balanced_weighted_avg":
            def ranking_calc(a, b, wa = 0.6, wb = 0.4):
                max_pert = max([i["pert_score"] for i in self._ordered])
                # Se il valore massimo di pertinenza è 0, lo si setta ad un
                # valore default = 1000, per abbattere il primo addendo ed
                # evitare divisione per 0.
                if max_pert == 0:
                    max_pert = 1000
                return (a / max_pert) * wa + b * wb
        else:
            raise ValueError("Selected ranking function not supported.")

        # Applica la funzione di ranking selezionata per il calcolo del ranking
        # complessivo.
        for i in self._ordered:
            final_score = ranking_calc(i["pert_score"], i["sent_score"])
            i.update({"final_score" : final_score})

        # Riordino finale, per score complessivo decrescente.
        self._ordered = sorted(
            self._ordered,
            key = lambda item : item["final_score"],
            reverse = True
            )

        
    def printResults(self, searcher, filename=sys.stdout):
        printer_params = [self._ordered, searcher.raw_query, self._sentiment]
        allowed = ["TxtPrinter", "OdsPrinter", "CsvPrinter"]
        """
        Metodo che crea la classe "Printer" in base al nome del file di output.
        Per esempio, se l'utente passa alla funzione "output.ods", il metodo
        crea la classe OdsPrinter che si occupa della formattazione corretta
        dei risultati su un file .ods.
        :param searcher:    Searcher, contiene la raw_query, utile da stampare
        :param filename:    File, il nome del file su cui scrivere. Di default,
                            si scrive su stdout.
        """
        # Caso particolare, stampa su stdout.
        if filename == sys.stdout:
            printer = TxtPrinter(*printer_params)
            printer.formatOutput(filename)
        else:
            ext = Path(filename).suffix[1:]
            name = "{}{}".format(ext.capitalize(), "Printer")
            if(name in allowed):               
                printer = globals()[name](*printer_params)
                printer.formatOutput(filename)
            else:
                raise Exception("Extension "+ str(ext) + " not supported.")
