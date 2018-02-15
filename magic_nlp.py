# Combines per-line source code comments into paragraph form.
# Christopher Siu (cesiu@calpoly.edu)
# CSC 570, Winter '18

import sys
from functools import reduce

# This is how the magic works:
import nltk
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')

# Define a grammar.
# TODO: I basically made this up as I went based on a high school knowledge of
#       linguistics. Considering the English language, I'm sure it's missing
#       some edge cases...
# TODO: It definitely does not consider declension or conjugation.
#       Gerunds are tagged as participles...that might be okay, actually.
#       Compound nouns can't be parsed.
#       At some point, we should allow commas to replace repeated conjunctions.
#       NLTK's tagging is really bad at confusing helping verbs for gerunds.
_verbs = ["VB", "VBD", "VBP", "VBZ"]
_grammar = nltk.CFG.fromstring("""
 Root -> NounP VerbP | NounP VerbP 'CC' Root | NounP | VerbP | 'UH'
 InfP -> 'TO' VerbP
NounP -> NounP 'CC' NounP | AdjP NounP | NounP AdjP | InfP | GerP | NounW
VerbP -> VerbP 'CC' VerbP | AdvP VerbP | VerbP AdvP | VerbP NounP | VerbP AdjP | VerbW
 AdjP -> AdvP AdjW | AdjW AdvP | InfP | PrepP | PartP | 'PDT' AdjW | AdjW
 AdvP -> AdvP AdvP | InfP | PrepP | AdvW
PrepP -> 'TO' NounP | 'IN' NounP
 GerP -> PartP
PartP -> PartP 'CC' PartP | AdvP PartP | PartP AdvP | PartP NounP | PartP AdjP | PartW
NounW -> 'NN' | 'NNS' | 'NNP' | 'NNPS' | 'PRP' | 'WP' | 'CD'
VerbW -> %s
 AdjW -> 'JJ' | 'JJR' | 'JJS' | 'PRP$' | 'WP$' | 'DT' | 'WDT' | NounP 'POS' | 'CD'
 AdvW -> 'RB' | 'RBR' | 'RBS' | 'MD'
PartW -> 'VBG' | 'VBN'
""" % " | ".join(["'%s'" % verb for verb in _verbs]))


# Tags and arses a string using a CFG.
# string - The string to parse
# cfg - The CFG with which to parse the string
# Returns a pair containing the first parse tree (or None if the string could
#  not be parsed) and the POS tags.
def parse(string, cfg):
    tags = nltk.pos_tag(nltk.word_tokenize(string))
    tree = next(nltk.ChartParser(cfg).parse([tag[1] for tag in tags]), None)
    return (tree, tags)


# Preprocesses strings, greedily combining pairs.
# strings - A list of strings
# Returns the preprocessed list of strings
def preproc(strings):
    return preproc_clauses(preproc_phrases(strings))


# Preprocesses strings, greedily combining "noun-verb" pairs.
# strings - A list of strings
# Returns the preprocessed list of strings
def preproc_clauses(strings):
    global _grammar

    if len(strings) < 2:
        return strings
    else:
        if is_noun_phrase(*parse(strings[0], _grammar)) \
           and is_verb_phrase(*parse(strings[1], _grammar)):
            return ["%s %s" % (strings[0], strings[1])] \
                    + preproc_clauses(strings[2:])
        else:
            return [strings[0]] + preproc_clauses(strings[1:])


# Preprocesses strings, greedily combining "noun-noun" and "verb-verb" pairs.
# strings - A list of strings
# Returns the preprocessed list of strings
def preproc_phrases(strings):
    global _grammar

    if len(strings) < 2:
        return strings
    else:
        if is_noun_phrase(*parse(strings[0], _grammar)) \
           and is_noun_phrase(*parse(strings[1], _grammar)) \
           or is_verb_phrase(*parse(strings[0], _grammar)) \
           and is_verb_phrase(*parse(strings[1], _grammar)):
            return preproc_phrases(["%s and %s" % (strings[0], strings[1])]
                                   + strings[2:])
        else:
            return [strings[0]] + preproc_phrases(strings[1:])


# Combines two strings.
# ind_str - The more significant of two strings
# dep_str - The less significant of two strings
# Returns a combination of the two strings.
def concat(ind_str, dep_str):
    global _debug, _grammar

    # If either string is empty, return the other.
    if ind_str == "":
        return dep_str
    elif dep_str == "":
        return ind_str
    else:
        # Construct parse trees for the two strings.
        ind_tree = parse(ind_str, _grammar)
        dep_tree = parse(dep_str, _grammar)

        if is_clause(*ind_tree):
            if is_clause(*dep_tree):
                # Both are clauses.
                return "%s and %s" % (ind_str, dep_str)
            else:
                # The first is a clause, the second is not.
                return "%s before %s" % (ind_str, dep_str)
        else:
            if is_clause(*dep_tree):
                # The second is a clause, the first is not.
                return "%s after %s" % (dep_str, ind_str)
            else:
                # Neither is a clause.
                return "%s and %s" % (ind_str, dep_str)


# Helps determine whether or not a string is a clause.
# tree - The string's CFG parse tree or None if it could not be parsed
# tags - The string's POS tags.
# Returns True if the string is a clause and False otherwise.
def is_clause(tree, tags):
    return tree is not None and len(tree) >= 2 \
           and tree[0].label() == "NounP" \
           and tree[1].label() == "VerbP"


# Helps determine whether or not a string is a noun phrase.
# tree - The string's CFG parse tree or None if it could not be parsed
# tags - The string's POS tags.
# Returns True if the string is a noun phrase and False otherwise.
def is_noun_phrase(tree, tags):
    global _verbs

    if tree is not None:
        return len(tree) == 1 and tree[0].label() == "NounP"
    else:
        return reduce(lambda p, tag: p and tag[1] not in _verbs, tags, True)


# Helps determine whether or not a string is a verb phrase.
# tree - The string's CFG parse tree or None if it could not be parsed
# tags - The string's POS tags.
# Returns True if the string is a verb phrase and False otherwise.
def is_verb_phrase(tree, tags):
    global _verbs

    if tree is not None:
        return len(tree) == 1 and tree[0].label() == "VerbP"
    else:
        return reduce(lambda p, tag: p or tag[1] in _verbs, tags, False)


def main(argv):
    paragraph = ""

    # TODO: This combines sentences linearly, one after the other. For better
    #       results, suggest combining in an order informed by the AST.
    with open(argv[1], "r") as string_file:
        strings = preproc([string.strip() for string in string_file])
        for string in strings:
            paragraph = concat(paragraph, string)

    print(paragraph)


if __name__ == "__main__":
    main(sys.argv)
