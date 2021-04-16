from nltk.corpus import wordnet

word = "give"
pos = wordnet.VERB
language = "eng"

syns = wordnet.synsets(word, pos=pos, lang=language)

# pos=VERB, NOUN, ADJ, ADV

synonyms = []
antonyms = []

for synset in syns:
    print("SYNSET NAME: "+str(synset.name()))

    for l in synset.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

    print("SYNONIMS: " + str(synonyms))
    print("ANTONYMS: " + str(antonyms))

    print("GLOSS: "+str(synset.definition()))
    print("EXAMPLES: "+str(synset.examples()))
    print("HYPERNYMS: "+str(synset.hypernyms()))
    print("-----------------")
    synonyms = []
    antonyms = []

print("\n\n")

from difflib import SequenceMatcher

#string1 = "Be_VBZ(Of_IN(Good_JJ(President_NN(x1)), United_NNP_States_NNP(x3)), Large_JJ(Cavity_NN(x2))) "
#string2 = "Cause_VBN(Large_JJ(Cavity_NN(x2)), Explosion_NNS(x4))"

#string1 = "Be_VBP(Crater_NNS(x1), Large_JJ(Cavity_NNS(x2)))"
#string2 = "Cause_VBN(Large_JJ(Cavity_NNS(x2)), Explosion_NNS(x3))"

#string1 = "Cause_VBN(Large_JJ(Cavity_NNS(x2)), Of_IN(Good_JJ(President_NN(x3)), United_NNP_States_NNP(x4)))"
#string2 = "Be_VBP(Crater_NNS(x1), Large_JJ(Cavity_NNS(x2)))"

string1 = "Be_VBZ(Man_NN(x1), Good_JJ(Man_NN(x2)))"
string2 = "Call_VBN(Man_NN(x1), Robert_NNP(x3))"

match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))

print(match)  # -> Match(a=0, b=15, size=9)
common = string1[match.a: match.a + match.size]

print("common: ", common)

while common[0] == "(":
    common = common[1:]
while common[-1] != ")":
    common = common[:len(common)-1]

print("common: ", common)

if str(string1).find("Cause_VBN") == -1:
    new = string1.replace(common, string2)
else:
    new = string2.replace(common, string1)

print(new)




#word_lemmas = wordnet.lemmas(word, pos=pos, lang=language)
#print("LEMMI: " + str(word_lemmas))


