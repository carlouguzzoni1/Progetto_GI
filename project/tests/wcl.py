from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re
import string
from wordcloud import WordCloud, STOPWORDS
import project.src.back_end.Database as dd
import project.src.back_end.IndexGenerator as ig
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from project.src.front_end.Results import Results
from project.src.front_end.Searcher import Searcher
import time
from PIL import Image


def create_wordcloud(text, file_name):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords).generate(text)

    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    # plt.show()
    plt.savefig(file_name)

q = input("Insert query > ")
sentiment = input("Insert sentiment (positive/negative) > ")
s = Searcher("handle", "text")
res = s.submit_query(q, results_threshold = 500)
r = Results("Vader", sentiment, res, ranking_fun = "balanced_weighted_avg")
r.printResults(s, "Wordclouds/output.ods")
# Noise is reduced by a lot, considering only the tweets where sentiment is relevant.
threshold = 0.2
text = ""
for tweet in r._ordered:
    if tweet["sent_score"] > threshold:
        text = text + tweet["text"]
text = text.replace("customer", "")
text = text.replace("service", "")
text = text.replace("USAirways", "")
text = text.replace("united", "")
text = text.replace("SouthwestAir", "")
text = text.replace("JetBlue", "")
text = text.replace("AmericanAir", "")
create_wordcloud(text, "Wordclouds/wordcloud.png")
