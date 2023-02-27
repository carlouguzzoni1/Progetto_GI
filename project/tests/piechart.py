import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer

from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher
import math
from functools import reduce

import matplotlib.pyplot as plt
import numpy as np

# Crea un'indice sul file originale.

query = input("Insert query > ")

db = dd.Database("./csv/airline.csv")
db.fillDb()
fields = ["handle", "text"]
db.filterFields(*fields)

schema_fields = {
    "handle"  : TEXT(stored = True, analyzer = StemmingAnalyzer()),
    "text"    : TEXT(stored = True, analyzer = StemmingAnalyzer())
        }

schema = Schema(**schema_fields)
ix = ig.IndexGenerator(schema, db)
ix.fillIndex()

s = Searcher("handle", "text", scoring_fun = "BM25F")
res = s.submit_query(query)
r = Results("Vader", "compound", res, ranking_fun = "balanced_weighted_avg")
r.printResults(s, "./piechart/output.txt")
r.printResults(s, "./piechart/output.ods")

positive = []
negative = []
neutral = []

for tweet in r._ordered:
    if tweet["sent_score"] < 0.05 and tweet["sent_score"] > -0.05:
        neutral.append(tweet)
    elif tweet["sent_score"] > 0.05:
        positive.append(tweet)
    else:
        negative.append(tweet)

sizes = ([len(categ) for categ in [positive, negative, neutral]])
mylabels = ["Positive", "Negative", "Neutral"]
plt.pie(sizes, labels=mylabels)
plt.show()
