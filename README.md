# TwOR
## (Twitter Opinion Retrieval)
TwOR is a framework written in python3 based on **whoosh**, specially made for **opinion retrieval**. It has been tested and used mainly for corpora made of tweets.

# Dependencies 
Theese dependencies are **mandatory**:
- whoosh
- tqdm
- pyexcel_ods3
- expertai-nlapi
- vaderSentiment
- transformers
- tensorflow

# Optional dependencies
- textblob
- matplotlib

# Quick start
+ Clone the repo;
+ Install the dependencies;
+ Install the package by running `./install.sh`;
+ To test the package with test scripts, change directory to `project/tests` then:
    + Run `indexing_script.py` to test index creation;
    + Run `query_script.py` to test queries;
        + Insert any query;
        + The default sentiment analysis tool is [**Vader**](https://github.com/cjhutto/vaderSentiment), which supports one of **positive** or **negative** as sentiment parameters;
        + If you want support for more sentiment categories, go to  [Queries](#queries);
        + Check `output.txt` or `output.ods` to see the results;
    + Run `benchmark.py` to test TwOR's performances;
    + Run `piechart.py` to check out a chart showing the sentiment distribution in the default corpora;
    + Run `wcl.py` to plot a nice wordcloud image from a set of query results;
    + Some of these test scripts are furtherly discussed in the follow-up;

# Indexing
```python
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
```

+ The `Database` objects is used to process raw data extracted from the csv file. The /csv contains 2 files downloaded from [Kaggle](https://www.kaggle.com/) used as an example.
Check our `presentation` fore more information on the dataset that has been used. 
+ The `filterFields` method is used to keep only the specified fields from the dataset. In      this case, we keep only the author and the text of the tweet.
+ The `IndexGenerator` object is used to create the Index. The `fillIndex` method fills the Index with documents. It might take some time according to the size of the documents.

# Queries
```python
from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher

query = input("Insert query > ")
sentiment = input("Insert sentiment > " )
s = Searcher("handle", "text", scoring_fun = "TF_IDF")
res = s.submit_query(query, results_threshold = 100, expand=False)
r = Results("Vader", sentiment, res, ranking_fun = "balanced_weighted_avg")
r.printResults(s, "output.txt")
r.printResults(s, "output.ods")
```

+ The `Searcher` object retrieves documents based on pertinence. Takes the fields that need to be scanned as arguments.
	+ To use a different **ranking function**, use the `scoring_fun` parameter. **TF_IDF** is used as default, but BM25F and PL2 are supported as well.
+ If you want to turn on query expansion (generally recommended), set `expand=True`. It's also possible to increment the maximum number of results by changing the `results_threshold` parameter;
+ The `Results` object gives a global ranking to the retrieved documents based on **pertinence** and **sentiment** scores. Takes the sentiment analysis tool as an argument, in this case Vader is used as default. For now 4 different tools are supported:
    + **Vader**: lexicon and rule-based tool that gives a score in a [-1,1] range, so that a "binary" classification can be applied (positive/negative or neutral).
    + [ExpertAI](https://pypi.org/project/expertai-nlapi/): API based on AI, supports different sentiment types.
    + [Roberta](https://huggingface.co/docs/transformers/model_doc/roberta); AI based, supports different sentiment types, check documentation for more information. For this tool, sentiment categories are:
	    + anger;
	    + disgust;
	    + fear;
	    + joy;
	    + neutral;
	    + sadness;
	    + surprise;
    + **Roberta2**: same as Roberta but uses a different pre-trained model that only gives a positive and negative score to the input text. Really usefull during benchmarking if you want to compare an AI-based approach (Roberta2) to a symbolic approach (Vader).

# Benchmarks
We extracted a random sample of 100 tweets using the `Database.getSample(self, n, ods=False, csv=False)`method, then we manually annotated a level of "satisfaction" in a [0-3] range for each tweet for each query, based on the user original need (pertinence and sentiment are both considered!). We tried to stay simple and think of common queries that users might actually submit, like the ones listed below. In this particular benchmark, the user is always looking for "positive" tweets.

+ *reviews on customer service*,
+ *sauvignon wine*,
+ *technical problems with flight*,
+ *quality of personal*,
+ *rerouting or rescheduling*, 
+ *late arrival*,
+ *tickets and bookings*,
+ luggage and bags,
+ departures and arrivals,
+ internet connection

If you want to see produced graphs, you can run the `benchmark.py` script yourself. 
The plotted graphs are saved in the `./BenchGraphs` folder.
`./sample_results` contains one output file for each one of the 10 submitted queries.
The **DCG** scores are encouraging, revealing that the ranking system is apparently decent. Identifying **sarcasm** is a big problem though, and cannot be solved easily without training a model with specific training sets. Even **Roberta** has some issues with sarcasm detection.
**Vader** has been used in the benchmarking script, but using Roberta does not considerably change the DCG scores.
Check out our `presentation` for more information.

Some more specific queries, that you can find in the `query_examples.py` script:
+ another AND trip,
+ internet OR connection OR wifi,
+ "good food"

# More stuff about tests
+ `piechart.py` contains a simple script that generates a sentiment-based piechart based on the input query. The output is saved in the `./piechart` folder.
+ `./sample_results` contains one output file for each query that has been tested during the benchmark.
+ `./samples` contains a random sample of 100 tweet that has been manually annotated to calculate the **DCG** score during the benchmark.
+ `./thesaurus/wn_s.pl` is the **Wordnet Thesaurus** that has been used for query expansion;
+ You can use the `wcl.py` script to visualize the most used words in certain types of tweets by creating a wordcloud. The default sentiment analysis tool used is Vader. The output will be stored in the `./Wordcloud` folder.
+ `ExampleOutput` contains the output of `./query_examples.py`.

## License
MIT
**Free Software**

