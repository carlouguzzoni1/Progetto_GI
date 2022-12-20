Documento riassuntivo del query language.

NB: da aggiornare ogni volta che viene cambiato qualcosa a livello di QueryParser, plugin e/o formattazione della query in ingresso.

- Il QL supporta query sia in AND che in OR, senza necessariamente doverlo specificare con gli operatori AND ed OR.
  In pratica, basta inserire la query in linguaggio naturale, se non si hanno particolari pretese.
  Per formulare query più sofisticate, vedere di seguito.
- Di default, si eseguono ricerche in OR dei termini nella query, incentivando i risultati in cui compaiono termini diversi, piuttosto che duplicati di un singolo termine.
  Il parametro che definisce questo comportamento si chiama "grouping factor", e deve avere un valore in [0,1].
  Di default lo si pone a 0.8, ma lo si può customizzare alla creazione di un oggetto Searcher.
- È necessario selezionare i campi sui quali eseguire le query. Naturalmente, è necessario che questi siano presenti nell'indice di ricerca.
  Nel caso una query non restituisse risultati, vengono stampati un massimo di 10 suggerimenti (default) per un'edit distance massimo pari a 2 (di default).
  I parametri menzionati sono inseriti all'interno del metodo __make_suggestions, nella classe Searcher, e non li si può ridefinire se non modificando il codice.
  Questa scelta è giustificata dal fatto di non volere suggerimenti troppo lunghi, né brevi, né differenti dai termini inseriti, anche in caso di typo.
- Per effettuare query di prossimità, scrivere il testo della query tra doppi apici (eg. "testo della query").

- Un elenco di formati più complessi di query, che si possono utilizzare, e che non sono ancora stati direttamente modificati, ma solo testati:
    - Wildcard query:
        - ?: "b?g" -> ritorna tutti i risultati contenenti "bag", "bug", "big", ...
        - *: "b*g" -> ritorna tutti i risultati contenenti "brag", "backlog", ... oltre a quelli della query "b?g".
        Si possono aggregare più wildcards in una stessa query, naturalmente a discapito delle prestazioni.
    - Range query:
        - "[duck TO duct]" -> ritorna tutti i risultati contenenti termini nell'intervallo.
        Uso delle parentesi:
            - Parentesi quadre -> estremi inclusi.
            - Parentesi graffe -> estremi esclusi.
        ATTENZIONE: le range query comportano un notevole overhead, specie se su un corpora ricco di documenti e vocaboli differenti. Sono quindi deprecate.
    - Boosting dei risultati:
        - "date^2 rate^0.5" -> raddoppia il rating di "date" e dimezza quello di "rate", nel computo effettuato da whoosh.
