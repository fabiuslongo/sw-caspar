import spacy
import neuralcoref
nlp = spacy.load('en_core_web_lg')
neuralcoref.add_to_pipe(nlp, greedyness=0.75)

doc = nlp("My sister has a dog. She loves him")

print(doc._.coref_clusters)
print(doc._.coref_resolved)