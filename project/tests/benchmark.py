SEPARATOR = "\n-----------------\n"


# Parte 1: costruzione dell'indice da un campione casuale preso dal corpora.
# Import necessari.
import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer


# Dizionario di query per il benchmarking.
queries = {
    "r1"    : "reviews on customer service",
    "r2"    : "sauvignon wine",                     # !
    "r3"    : "technical problems with flight",
    "r4"    : "quality of personal",
    "r5"    : "rerouting or rescheduling",          # !
    "r6"    : "late arrival",                       # !
    "r7"    : "tickets and bookings",
    "r8"    : "luggage and bags",
    "r9"    : "departures and arrivals",
    "r10"   : "internet connections",
    }

# Costruzione della struttura dati Database.
db = dd.Database("./samples/dcg_sample.csv")
# Il file dcg_sample è stato generato casualmente, ma i valori di soddisfazione per
# la DCG sono stati manualmente annotati per tutte e 10 le query.
db.fillDb()
fields = ["handle", "text"]
fields.extend(list(queries.keys()))
db.filterFields(*fields)

# Costruzione dello schema dell'indice.
schema_fields = {
    "handle"  : TEXT(stored = True, analyzer = StemmingAnalyzer()),
    "text"    : TEXT(stored = True, analyzer = StemmingAnalyzer())
        }

# Per abilitare stopwords, inserire:
# stoplist = None, minsize = 0
# come parametri nel costruttore di StemmingAnalyzer.

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
# Per variare funzione di scoring aggiungere scoring_fun = "template" come
# parametro, al costruttore di Searcher. Supportate: TF_IDF (default), PL2
# BM25F.
s = Searcher("handle", "text", scoring_fun = "TF_IDF")


def count_dcg(ordered, field):
    """Calcola la DCG del nostro sistema di IR."""
    li = [int(i[field]) for i in ordered]
    num_results = len(li)
    l = [li[idx] / math.log(idx + 2, 2) if idx != 0 else li[idx] for idx in range(num_results)]
    return reduce(lambda x, y : x + y, l)


# Struttura dati per la stampa finale.
dcg_data = []
ndcg_data = []
tweets_returned = []
counter = 1

# Sottomissione, una ad una, delle query pre-impostate.
for k, v in queries.items():
    res = s.submit_query(v, expand = True)
    try:
        print(k)
        # Per variare funzione di ranking aggiungere ranking_fun = "template"
        # come parametro, al costruttore di Results. Supportate: naive
        # (default), "balanced_weighted_avg".
        r = Results("Vader", "compound", res, ranking_fun = "balanced_weighted_avg")
        # Calcolo del ranking ottimale per la NDCG.
        optimal_ranking = sorted(r.ordered, key = lambda d: d[k], reverse = True)
        dcg = count_dcg(r.ordered, k)
        optimal_dcg = count_dcg(optimal_ranking, k)
        ndcg = dcg / optimal_dcg
        dcg_data.append((queries[k], dcg))
        ndcg_data.append((queries[k], ndcg))
        print(
            "Query:", queries[k], "\n",
            "; measured DCG value:", dcg, "\n",
            "; optimal DCG value:", optimal_dcg, "\n",
            "; NDCG value:", ndcg
            )
        tweets_returned.append(len(r.ordered))
    except:
        dcg_data.append((queries[k], 0))
        ndcg_data.append((queries[k], 0))
        tweets_returned.append(0)
        print("Query:", queries[k], "\n",
              "; measured DCG value: 0", "\n",
              "; optimal DCG value: 0", "\n",
              "; NDCG value: 0 \t NO RESULTS"
              )
    finally:
        with open("./sample_results/query" + str(counter) + ".txt", "w") as f:
            for element in r.ordered:
                f.write(str(element) + "\n" + SEPARATOR)
        counter += 1
        print("\n")


print(dcg_data)
print(ndcg_data)

# Parte 3: plotting dei risultati.
# Import necessari.
import matplotlib.pyplot as plt
import numpy as np


def custom_plot(data, parameter, file_name):
    """Stampa i grafici per DCG/NDCG."""
    # Asse x: query.
    qrs = ["q{}".format(i) for i in range(1, len(queries) + 1)]
    # Asse y: valore DCG/NDCG (all'indice 1 nella tupla).
    vls = [round(element[1], 1) for element in data]
    print(vls)
    # Creazione del plot.
    x = np.arange(len(qrs))
    width = 0.35
    fig, ax = plt.subplots()
    rec1 = ax.bar(x - width / 2, vls, width, label = parameter)
    rec2 = ax.bar(
        x + width / 2, tweets_returned, width, label = 'num. of retrieved tweets'
        )
    ax.set_ylabel('Val')
    ax.set_title(parameter + " TF-IDF")
    ax.set_xticks(x, qrs)
    ax.legend()
    ax.bar_label(rec1, padding = 5)
    ax.bar_label(rec2, padding = 5)
    fig.tight_layout()
    plt.savefig(file_name)
    plt.show()    # Abilita stampa grafico a run-time, su apposita finestra.


# Stampa dei grafici.
custom_plot(dcg_data, "DCG", "./bench_graphs/dcg_TF-IDF.png")
custom_plot(ndcg_data, "NDCG", "./bench_graphs/ndcg_TF-IDF.png")
