# Twitter opinion retrieval system

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

A sample project that exists as an aid to the [Python Packaging User
Guide][packaging guide]'s [Tutorial on Packaging and Distributing
Projects][distribution tutorial].

This project does not aim to cover best practices for Python project
development as a whole. For example, it does not provide guidance or tool
recommendations for version control, documentation, or testing.

[The source for this project is available here][src].

The metadata for a Python project is defined in the `pyproject.toml` file, 
an example of which is included in this project. You should edit this file
accordingly to adapt this sample project to your needs.

----
[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/pypa/sampleproject
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# Installazione
## Installazione automatica
Per installare in modo rapido il software basta eseguire lo script `install.sh`.
In caso di problemi, si può rimuovere il software eseguendo lo script `uninstall.sh`.
## Installazione manuale
Per installare il software manualmente, ci si può posizionare all'interno della cartella `dist` e usare
il seguente comando:
```sh
python3 -m pip install sampleproject-3.0.0-py3-none-any.whl
```

# Esempio di esecuzione
## Creazione dell'indice
Per indicizzare correttamente un file .csv, è necessario posizionarlo all'interno di una cartella chiamata `csv`
a sua volta contenuta nella cartella corrente di lavoro (dove è stata lanciata la shell python).
Nell'esempio riportato si fa riferimento al file './csv/airline.csv', scaricabile insieme ad altri file
d'esempio da questo link: https://github.com/theElandor/csv .


```python 
import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer


# Creazione di un oggetto Database.
db = dd.Database('./csv/airline.csv')
# Popolazione del Database.
db.fillDb()
# Selezione dei campi da indicizzare.
db.filterFields('handle','text')
db.getSample(50, ods=True, csv=True)


# Creazione dello schema per l'indice Whoosh.
schema = Schema(
    handle = TEXT(stored = True, analyzer = StemmingAnalyzer()),
    text = TEXT(stored = True, analyzer = StemmingAnalyzer())
    )

# Creazione dell'indice.
i = ig.IndexGenerator(schema, db)
# Popolazione dell'indice.
i.fillIndex()
```
## Interrogazione tramite query
```python
from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher

# Creazione del Searcher.
s = Searcher("handle", "text")

# Estrazione dei risultati con inserimento di una query.
res = s.submit_query("american airline")
# Elaborazione dei risultati in un oggetto Results, tramite lo strumento
# di sentiment analysis Vader, impostato per il sentiment complessivo.
r = Results("Vader", "compound", res)
r.printResults(s, "output.txt") 

# Si ripete la procedura appena vista.
res2 = s.submit_query("service on board")
r2 = Results("Vader", "compound", res2)
r2.printResults(s, "output2.txt")

```
## Benchmarking
Il software contiene anche uno script di benchmarking pre-installato, per valutare l'efficacia del
sistema di Opinion Retrieval e come ulteriore esempio di utilizzo dei tool da noi creati.
Il sistema di valutazione adottato è il **DCG** (*Distance Comulative Gain*), basato su un campione casuale
di 50 Tweet i cui valori di rilevanza rispetto alle query sono stati generati casualmente per ragioni didattiche.
Per studiare effettivamente le performance, basta modificare il file csv generato dal metodo **sample** dell'oggetto `Database` inserendo le annotazioni a mano.

```python
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
```
