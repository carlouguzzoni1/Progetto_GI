"""
Example indexing script.
"""

import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer


db = dd.Database('./csv/airline.csv')
db.fillDb()
db.filterFields('handle','text')
schema = Schema(
    handle = TEXT(stored = True, analyzer = StemmingAnalyzer()),
    text = TEXT(stored = True, analyzer = StemmingAnalyzer())
    )
i = ig.IndexGenerator(schema, db)
i.fillIndex()
