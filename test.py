from owlready2 import *

try:
    my_onto = get_ontology("drugs.owl").load()
    print("\nLoading existing drugs.owl...")
except IOError:
    my_onto = get_ontology("http://test/drugs.owl")
    print("\nCreating new drugs.owl...")

with my_onto:
    class Contraindication(Thing):
        pass

    class Drug(Thing):
        pass

    class Disorder(Thing):
        pass

    class has_for_drug(ObjectProperty):
        pass

    class has_for_disorder(ObjectProperty):
       pass

    class contraindicated_with(ObjectProperty):
       pass

    class contraindicates(ObjectProperty):
       pass



ci1 = Contraindication()
ci2 = Contraindication()
ci3 = Contraindication()
ci4 = Contraindication()

Ticagrelor = types.new_class("Ticagrelor", (Drug,))
Heparin = types.new_class("Heparin", (Drug,))
Aspirin = types.new_class("Aspirin", (Drug,))

HemorrhagicDisorder = types.new_class("HemorrhagicDisorder", (Disorder,))
AcquiredHemorrhagicDisorder = types.new_class("AcquiredHemorrhagicDisorder", (Disorder,))
ConstitutiveHemorrhagicDisorder = types.new_class("ConstitutiveHemorrhagicDisorder", (Disorder,))


Ticagrelor.contraindicated_with = [ci1]
Heparin.contraindicated_with = [ci2]
Aspirin.contraindicated_with = [ci3, ci4]

HemorrhagicDisorder.contraindicates = [ci1]
AcquiredHemorrhagicDisorder.contraindicates = [ci3]
ConstitutiveHemorrhagicDisorder.contraindicates = [ci2, ci4]


with my_onto:
    class DisorderContraindicatingAspirin(Drug):
        equivalent_to = Disorder & contraindicates.some(Aspirin) & has_for_drug.some(Aspirin)

    class DisorderOkWithAspirin(Drug):
        equivalent_to = Not(Disorder & contraindicates.some(Aspirin) & has_for_drug.some(Aspirin))


close_world(Contraindication)
close_world(Drug)

print(issubclass(ConstitutiveHemorrhagicDisorder, Disorder))

print(issubclass(HemorrhagicDisorder, DisorderOkWithAspirin))
print(issubclass(AcquiredHemorrhagicDisorder, DisorderOkWithAspirin))
print(issubclass(ConstitutiveHemorrhagicDisorder, DisorderOkWithAspirin))

print(issubclass(HemorrhagicDisorder, DisorderContraindicatingAspirin))
print(issubclass(AcquiredHemorrhagicDisorder, DisorderContraindicatingAspirin))
print(issubclass(ConstitutiveHemorrhagicDisorder, DisorderContraindicatingAspirin))

my_onto.save(file="drugs.owl", format="rdfxml")


a = "a1975"
if a[0] in ['0','1','2', '3', '4', '5', '6', '7', '8', '9']:
    a = 'N'+a
print(a)