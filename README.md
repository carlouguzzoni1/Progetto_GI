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

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/pypa/sampleproject
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# Creation of the Index
Down below you can find an example code that shows how to create a Index. Remember that you will always need a folder called "csv" in the directory where you are using the python shell, containing the csv files. You can download an example folder from here https://github.com/theElandor/csv.

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
# Example of usage
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