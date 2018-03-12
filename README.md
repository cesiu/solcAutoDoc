### NLP Magic

`magic_nlp.py` attempts to combine lines into a single sentence.

`python3 magic_nlp.py <filename>`

It also supports redirection.

`cat <filename> | python3 magic_nlp.py -`

### Solidity Parsing

`parser.py` attempts to generate documentation for Solidity files, occasionally applying some NLP magic. 

`python3 parser.py solidityFiles/simpleAuction.json`
