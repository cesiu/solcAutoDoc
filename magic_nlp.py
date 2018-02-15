# Combines per-line source code comments into paragraph form.
# Christopher Siu (cesiu@calpoly.edu)
# CSC 570, Winter '18

import sys
# This is how the magic works:
import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')


# Define a grammar.
# TODO: I basically made this up as I went based on a high school knowledge of
#       linguistics. Considering the English language, I'm sure it's missing
#       some edge cases...
# TODO: It definitely does not consider declension or conjugation, and gerunds
#       are considered the same as participles.
_grammar = nltk.CFG.fromstring("""
    S -> S '.' | NounP VerbP | NounP | VerbP | 'UH'
 InfP -> 'TO' VerbP
NounP -> NounP 'CC' NounP | AdjP NounP | NounP AdjP | InfP | GerP | NounW
VerbP -> VerbP 'CC' VerbP | AdvP VerbP | VerbP AdvP | VerbP NounP | VerbP AdjP | VerbW
 AdjP -> AdvP AdjW | AdjW AdvP | InfP | PrepP | PartP | 'PDT' AdjW | AdjW
 AdvP -> AdvP AdvP | InfP | PrepP | AdvW
PrepP -> 'IN' NounP
 GerP -> PartP
PartP -> PartP 'CC' PartP | AdvP PartP | PartP NounP | PartW
NounW -> 'NN' | 'NNS' | 'NNP' | 'NNPS' | 'PRP' | 'WP' | 'CD'
VerbW -> 'VB' | 'VBN' | 'VBP' | 'VBZ'
 AdjW -> 'JJ' | 'JJR' | 'JJS' | 'PRP$' | 'WP$' | 'DT' | 'WDT' | NounP 'POS' | 'CD'
 AdvW -> 'RB' | 'RBR' | 'RBS' | 'MD'
PartW -> 'VBG' | 'VBN'
""")


def main(argv):
    tags = nltk.pos_tag(nltk.word_tokenize(argv[1]))
    trees = nltk.ChartParser(_grammar).parse([tag[1] for tag in tags])

    print("\nParsing \"%s\"...\n" % argv[1])

    # Right, this is a generator...
    success = False
    for tree in trees:
        success = True
        print(tree)

    if not success:
        print("ERROR: Could not parse \"%s\".\n"
              "    Tagged as: %s"
              % (argv[1], tags))

if __name__ == "__main__":
    main(sys.argv)
