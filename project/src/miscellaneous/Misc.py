"""Funzioni accessorie di vario tipo."""

import re
import time

def RemoveLinkFromText(text):
    """Rimuove gli URL da un campo testuale."""
    new_text = text
    url_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"
    for match in re.findall(url_pattern, text):
        new_text = new_text.replace(match, '')

    return new_text


def time_function(function):
    """Decoratore per la stampa del tempo di esecuzione di una funzione."""
    def new_function(*args, **kwargs):
        start = time.time()
        value = function(*args, **kwargs)
        end = time.time()
        print ("Function: " + str(function))
        print("Execution time: " + str(end - start))
        return value

    return new_function
