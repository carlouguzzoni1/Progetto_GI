"""
Script dimostrativo per le classi front-end: Searcher e Results.
Crea un oggetto Searcher, gli sottopone una query e stampa i risultati,
ordinati secondo una formula che mischia i punteggi di pertinenza e
sentiment. Viene infine fatta una stampa su file di testo.
La procedura è ripetuta per una seconda query, differente dalla prima.
"""

from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher


query = input("Insert query > ")
sentiment = input("Insert sentiment > " )
s = Searcher("handle", "text", scoring_fun = "TF_IDF")
res = s.submit_query(query, results_threshold = 100, expand=True)
r = Results("Vader", sentiment, res, ranking_fun = "balanced_weighted_avg")
r.printResults(s, "output.txt")
r.printResults(s, "output.ods")
