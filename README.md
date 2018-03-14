# Automatic Documentation of Solidity Code
Eric LaBouve, Chris Siu, Justin Kehl, Lenoy Avidan
California Polytechnic University: San Luis Obispo
CSC570: Winter 2018

## Abstract
Soldity is a programming language built on top of the Ehtereum blockchain that allows individuals to write smart contracts. Smart contracts are similar to traditional contracts in that they are a binding agreement between multiple parties, except they are written in code and are self executing. Reading and understanding a traditional contract is hard, so reading a coded contract most likely harder if someone is not an experienced programmer. We experiment with auto documentation of Solidity contracts to help readers understand the contents of Solidity contracts. Although the output text is verbose, there are many cases where the documentation produced through our program helped individuals understand the code they were reading.

## Introduction
Smart contracts are coded contracts that allow for binding agreements between multiple parties. Although most people do not know how to read code, it is still important for these people to understand these contracts. Even with human written descriptions for smart contracts it is possible for the writer to either misinterpret the code or purposely misconstrue the true meaning of the contract. Our group is researching techniques to interpret smart contract code and turn it into English text. We are working in the Solidity language which is hosted on the Ethereum blockchain.

## Background
The Solidity language documentation can be found [here](https://solidity.readthedocs.io/en/v0.4.21/)
This project falls in the domain of natural language processing, tree searching algorithms, and linguistics. Natural language processing is a large field of study in artificial intelligence and for our project, we take advantage of a python library called nltk. 
There has been some research into converting Java code into human readable method, class, and project descriptions [2, 3]. Paul W McBurney and Collin McMillan experimented with converting Java code into these descriptions and came up with positive results. These, however, depended on very descriptive and simple function and variable names. There is still a lot more research into methods of translating code to human readable language that can be done. There has been other research into automating descriptions based on online forums but that doesn’t really apply here [1]. Additionally, there has been research into breaking up variable names based on standard naming conventions and using the result to help describe the context of the variable [4]. There has also been a lot of research into Natural Language Processing (NLP) and Natural Language Generation (NLG) for creating grammatically correct and human readable sentences [5]. In fact there are many libraries for NLP, like for instance NLTK for python and Google’s NLP.

## parser.py
Solidity ships with a compiler, “solc”, whose responsibility is to compile smart contracts for running on the EVM. In the process, it builds an abstract syntax tree. The Solidity compiler recognizes two flags, “--ast-json” and “--ast-compact-json”, that cause it to dump its constructed ASTs to stdout in JSON. parser.py parses the json output from the --ast-compact-json command much like a traditional compiler would. It traverses through the tree in chronological order as it appears in the original text document. Documentation for the AST is largely unavailable, but we have documented much of the output [here](https://docs.google.com/document/d/1wZMqwrWrSe-UF3FvPnBO2lryz99_jbrpjYckSAb1qhU/edit?usp=sharing).

Once we have obtained an AST that represents the structure of the Solidity code, the tree is to be handed to our parser program. At a high level, the parser converts pieces of the AST to english phrases and/or groups of words. These groups of words serve as a direct translation of how an experienced Solidity program would read the text outloud to him/her self. Although the original intent of parser.py was to specifically focus on lines of code that deal with transactions, it was soon discovered that all lines of code -in some way or another- may influence the transfer of Ethereum coin from one party to another. The version that appears in this repository also only deals with logical lines of code inside methods. An example output from the program is what follows: 

'bankDeposits[msg.sender] += msg.value'

This line of text would translate into: Bank deposits from the ethereum sender gains money sent by the sender

Each description corresponding to the line of code will then be stored in a json data structure that can be used for future AST evaluation. For the sake of our program, the output is simply passed to our other program, magic_nlp.py, which formats the parser.py output according to English context free grammar rules, supported by python's nltk library.

## magic_nlp.py
Once the parser produces the phrases describing segments of code, we need to be able to take them and put them together into a human readable and grammatically correct format. 

## CHRIS GIVE YOUR DESCRIPTION HERE

## lda_topics.py
Although it was a failed attempt in practice, the theoretical idea was to use Latent Dirichlet Allocation (LDA) to discover topic-wide themes in the contract. LDA is an unsupervised, generative, statistical model that attempts to cluster related text into a chosen number of topics. The original idea was to cluster variable names discovered in the contract and build a vector from them. Using this vector, we can then compute a similarity between it and other documents, such as documents on Wikipedia to identify similar articles. The idea failed because programmers do not always use descriptive variable names, and this lead to innacurate results. This part of the project was abandoned shortly afterwards.

## Evaluation Criteria
We recognize that evaluation of natural language output is largely subjective because we intend to have our system evaluated by students who are partially and fully familiar with programming. Our system will be evaluated using the following criteria:
1. Descriptions produced are human readable. We have people read the descriptions and rate on a scale of 1 to 5 where 1 is “can’t understand the description” and 5 is “description is perfectly understood.”
2. Descriptions produced properly describe the code segment. Rated from scale of 1 to 5 where 1 is “description has no relation to code segment” and 5 is “description perfectly describes the code segment.”
3. Descriptions produced are concise. Rated from a scale of 1 to 5 where 1 is “description has many excess words” and 5 is “description has no excess words.”
4. Any additional comments abou the contract and output text.


## Results
The results of the study can be found [here](https://docs.google.com/spreadsheets/d/16RqYyBzWThm0wHQeoIkOsBNGLkTVI0JxwzLF7e5nnUI/edit?usp=sharing)

## References:
[1] Edmund Wong, Jinqiu Yang, and Lin Tan. AutoComment: Mining Question and Answer Sites for Automatic Comment Generation. 

[2] Paul W. McBurney and Collin McMillan. Automatic Documentation Generation via Source Code Summarization of Method Context

[3] Giriprasad Sridhara, Emily Hill, Divya Muppaneni, Lori Pollock and K. Vijay-Shanker. Towards Automatically Generating Summary Comments for Java Methods

[4] E. Hill, Z. P. Fry, H. Boyd, G. Sridhara, Y. Novikova,L. Pollock, and K. Vijay-Shanker. AMAP: Automatically Mining Abbreviation Expansions in Programs to Enhance Software Maintenance Tools. Intl Working Conf on Mining Software Repositories (MSR)

[5] NLP Research at Google


## Execution Instructions
### NLP Magic

`magic_nlp.py` attempts to combine lines into a single sentence.

`python3 magic_nlp.py <filename>`

It also supports redirection.

`cat <filename> | python3 magic_nlp.py -`

### Solidity Parsing

`parser.py` attempts to generate documentation for Solidity files, occasionally applying some NLP magic. 

`python3 parser.py solidityFiles/simpleAuction.json`
