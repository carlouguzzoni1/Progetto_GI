from Main.Results import Results
from Main.Searcher import Searcher


queries = [
    "another AND trip",
    "internet OR connection OR wifi",
    "\"good food\""
]
s = Searcher("handle", "text")
for i,q in enumerate(queries):
    res = s.submit_query(q, results_threshold = 20, expand=False)
    r = Results("Vader", "positive", res)
    r.printResults(s, "./ExampleOutput/q"+str(i+1)+".txt")
    r.printResults(s, "./ExampleOutput/q"+str(i+1)+".ods")
