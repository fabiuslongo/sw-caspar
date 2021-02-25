from phidias.Main import *
from phidias.Types import *
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


def_vars('X', 'Y', 'Z', 'T', 'W', 'K', 'J', 'M', 'N', "D", "I", "V", "L", "O", "E", "U", "S")

from actions import *
from mst_builder import *
from onto_builder import *
from direct_cmd_parser import *
from routines_parser import *
from smart_env_int import *
from front_end import *



# instantiate the engine
PHIDIAS.run()
# run the engine shell
PHIDIAS.shell(globals())
