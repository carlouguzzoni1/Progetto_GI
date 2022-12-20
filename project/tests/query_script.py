"""
Script dimostrativo per le classi front-end: Searcher e Results.
Crea un oggetto Searcher, gli sottopone una query e stampa i risultati,
ordinati secondo una formula che mischia i punteggi di pertinenza e
sentiment. Viene infine fatta una stampa su file di testo.
La procedura è ripetuta per una seconda query, differente dalla prima.
"""

from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher

# Creazione del Searcher.
s = Searcher("handle", "text")

# Estrazione dei risultati con inserimento di una query.
res = s.submit_query("american food")
# Elaborazione dei risultati in un oggetto Results, tramite lo strumento
# di sentiment analysis Vader, impostato per il sentiment complessivo.
r = Results("Vader", "compound", res)
r.printResults(s, "output.txt") 

# Si ripete la procedura appena vista.
res2 = s.submit_query("service on board")
r2 = Results("Vader", "compound", res2)
r2.printResults(s, "output2.txt")
