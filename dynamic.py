from owlready2 import *

try:
    my_onto = get_ontology("west.owl").load()
except IOError:
    my_onto = get_ontology("http://test/west.owl")



with my_onto:
 class Action(Thing):
     pass

 class Adjective(Thing):
       pass

 class Entity(Thing):
     pass

 class Preposition(Thing):
       pass

 class hasAdj(ObjectProperty):
      pass

 class hasObject(ObjectProperty):
      pass

 class hasSubject(ObjectProperty):
      pass

 class hasPrep(ObjectProperty):
      pass



print("\nClasses list:\n")
print(Action)
print(Adjective)
print(Entity)
print(Preposition)

with my_onto:
    my_new_classes = []
    my_new_classes.append(types.new_class("Sell_VBZ", (Action,)))
    my_new_classes.append(types.new_class("Hostile_JJ", (Adjective,)))
    my_new_classes.append(types.new_class("American_NN", (Entity,)))
    my_new_classes.append(types.new_class("Colonel_West_NNP", (Entity,)))
    my_new_classes.append(types.new_class("Criminal_NN", (Entity,)))
    my_new_classes.append(types.new_class("Cuba_NNP", (Entity,)))
    my_new_classes.append(types.new_class("Nation_NN", (Entity,)))
    my_new_classes.append(types.new_class("Weapon_NNPS", (Entity,)))
    my_new_classes.append(types.new_class("To_IN", (Preposition,)))


    print("\nSubclasses list:\n")

    for c in my_new_classes:
        print(c)  # qwerty.NewClassName

    my_obj = []
    my_obj.append(my_new_classes[0]("Sell"))
    my_obj.append(my_new_classes[1]("Hostile"))
    my_obj.append(my_new_classes[2]("American"))

    # Colonel_West type Colonel_West_NNP
    my_obj.append(my_new_classes[2]("Colonel_West"))
    # Colonel_West type American_NN
    my_obj.append(my_new_classes[3]("Colonel_West"))

    my_obj.append(my_new_classes[4]("Criminal"))

    # Cuba type Cuba_NNP
    my_obj.append(my_new_classes[5]("Cuba"))
    # Cuba type Nation_NN
    my_obj.append(my_new_classes[6]("Cuba"))

    my_obj.append(my_new_classes[6]("Nation"))

    my_obj.append(my_new_classes[7]("Missiles"))
    my_obj.append(my_new_classes[8]("To"))

    print("\nIndividuals list:\n")


    print("\nAssertions list:\n")

    # Cuba hasAdj Hostile
    my_obj[6].hasAdj = [my_obj[1]]
    print(my_obj[6], hasAdj, my_obj[6].hasAdj)

    # Sell hasPrep To
    my_obj[0].hasPrep = [my_obj[10]]
    print(my_obj[0], hasPrep, my_obj[0].hasPrep)

    # Sell hasSubj Colonel_West
    my_obj[0].hasSubject = [my_obj[3]]
    print(my_obj[0], hasSubject, my_obj[0].hasSubject)

    # Sell hasObj Missiles
    my_obj[0].hasObject = [my_obj[9]]
    print(my_obj[0], hasObject, my_obj[0].hasObject)

    # To hasObj cuba
    my_obj[10].hasObject = [my_obj[6]]
    print(my_obj[10], hasObject, my_obj[10].hasObject)

    # Asserting SWRL rule
    rule = Imp()
    rule.set_as_rule("""hasSubject(?x2, ?x1), American_NN(?x1), Weapon_NNPS(?x3), hasObject(?x2, ?x3), Sell_VBZ(?x2), hasPrep(?x2, ?x4), To_IN(?x4), hasObject(?x4, ?x5), Nation_NN(?x5), hasAdj(?x5, ?x6), Hostile_JJ(?x6) -> Criminal_NN(?x1)""")

    print("\nRule")

    print("body: ", rule.body)
    print("head: ", rule.head)

#my_onto.save(file="west.owl", format="rdfxml")


with my_onto:
  sync_reasoner_pellet() #sincronizziamo il ragionatore e mettiamo le inferenze dentro l'ontologia onto
  my_onto.save(file="west.owl", format="rdfxml")
  pass


print("SPARQL")

my_world = owlready2.World()
my_world.get_ontology("west.owl").load()  # path to the owl file is given here

graph = my_world.as_rdflib_graph()

result = list(graph.query("""Select ?p WHERE {<http://test/west.owl#Colonel_West> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?p .}"""))
for i in result:
    print(i)

result = list(graph.query("ASK WHERE {<http://test/west.owl#Colonel_West> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://test/west.owl#Criminal_NN>.}"))
print(result)




