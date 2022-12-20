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

db = dd.Database('./csv/airline.csv')
db.fillDb()
db.filterFields('handle','text')
db.getSample(50, ods=True, csv=True)

schema = Schema(
    handle = TEXT(stored = True, analyzer = StemmingAnalyzer()),
    text = TEXT(stored = True, analyzer = StemmingAnalyzer())
    )

i = ig.IndexGenerator(schema, db)
i.fillIndex()
```
## Interrogazione tramite query

```python
from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher


s = Searcher("handle", "text")

res = s.submit_query("american airline")
r = Results("Vader", "compound", res)
r.printResults(s, "output.txt") 

res2 = s.submit_query("service on board")
r2 = Results("Vader", "compound", res2)
r2.printResults(s, "output2.txt")
```