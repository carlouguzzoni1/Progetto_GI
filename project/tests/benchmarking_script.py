"""
Script di prova per le attività di benchmarking.
"""


# Parte 1: costruzione dell'indice da un campione casuale preso dal corpora.
# Import necessari.
import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer


# Dizionario di query per il benchmarking.
queries = {
    "r1"    : "reviews on customer service",
    "r2"    : "what people think about food on board",
    "r3"    : "technical problems with flight",
    "r4"    : "quality of personal",
    "r5"    : "risks and dangers when flying",
    "r6"    : "experience and panorama",
    "r7"    : "tickets and bookings",
    "r8"    : "luggage and bags",
    "r9"    : "responses and replies",
    "r10"   : "internet connection",
    }

# Costruzione della struttura dati Database.
db = dd.Database("sample.csv")
db.fillDb()
fields = ["handle", "text"]
fields.extend(list(queries.keys()))
db.filterFields(*fields)

# Costruzione dello schema dell'indice.
schema_fields = {
    "handle"  : TEXT(stored = True, analyzer = StemmingAnalyzer()),
    "text"    : TEXT(stored = True, analyzer = StemmingAnalyzer())
        }

for i in queries.keys():
    schema_fields[i] = eval("NUMERIC(stored = True, numtype = int)")

schema = Schema(**schema_fields)

# Costruzione dell'indice.
ix = ig.IndexGenerator(schema, db)
ix.fillIndex()


# Parte 2: sottomissione delle query all'indice precedentemente costruito,
# estrazione dei risultati e valutazione del sistema di IR tramite DCG.
# Import necessari.
from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher
import math
from functools import reduce


# Creazione del Searcher.
s = Searcher("handle", "text")


def count_dcg(ordered, field):
    """Calcola la DCG del nostro sistema di IR."""
    li = [int(i[field]) for i in ordered]
    num_results = len(li)
    l = [li[idx] / math.log(idx + 1) if idx != 0 else li[idx] for idx in range(num_results)]
    return reduce(lambda x, y : x + y, l)


# Struttura dati per la stampa finale.
final_data = []

for k, v in queries.items():
    res = s.submit_query(v)
    try:
        r = Results("Vader", "compound", res)
        print("Query:", queries[k], "; valore DCG:", count_dcg(r.ordered, k))
        final_data.append((queries[k], count_dcg(r.ordered, k)))
    except:
        final_data.append((queries[k], 0))
    

# Parte 3: plotting dei risultati.
# Import necessari.
import matplotlib.pyplot as plt


# Asse x: query.
qrs = ["q{}".format(i) for i in range(1, len(queries) + 1)]
# Asse y: valore DCG (all'indice 1 nella tupla).
vls = [element[1] for element in final_data]
# Creazione del plot.
fig = plt.figure(figsize = (10, 5))
plt.bar(qrs, vls, color ='blue', width = 0.4)

# Creazione delle etichette di plot ed assi.
plt.xlabel("Queries")
plt.ylabel("DCG score")
plt.title("Distance Cumulative Gain")
# Salvataggio del plot su file.
plt.savefig("bench.png")
