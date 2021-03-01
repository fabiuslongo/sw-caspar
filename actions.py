from parse_en import *
from nl_to_fol import *


from phidias.Types import *
import configparser
import math
from difflib import SequenceMatcher
import pyttsx3
import winsound
import itertools
from datetime import datetime


from owlready2 import *

try:
    my_onto = get_ontology("west.owl").load()
except IOError:
    my_onto = get_ontology("http://test/west.owl")



with my_onto:
 class Verb(Thing):
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

my_onto.save(file="west.owl", format="rdfxml")



config = configparser.ConfigParser()
config.read('config.ini')

cnt = itertools.count(1)
dav = itertools.count(1)

VERBOSE = config.getboolean('PARSING', 'VERBOSE')
LANGUAGE = config.get('PARSING', 'LANGUAGE')
ASSIGN_RULES_ADMITTED = config.getboolean('PARSING', 'ASSIGN_RULES_ADMITTED')

WAIT_TIME = config.getint('AGENT', 'WAIT_TIME')
LOG_ACTIVE = config.getboolean('AGENT', 'LOG_ACTIVE')

INCLUDE_ACT_POS = config.getboolean('POS', 'INCLUDE_ACT_POS')
INCLUDE_NOUNS_POS = config.getboolean('POS', 'INCLUDE_NOUNS_POS')
INCLUDE_ADJ_POS = config.getboolean('POS', 'INCLUDE_ADJ_POS')
INCLUDE_PRP_POS = config.getboolean('POS', 'INCLUDE_PRP_POS')
INCLUDE_ADV_POS = config.getboolean('POS', 'INCLUDE_ADV_POS')
OBJ_JJ_TO_NOUN = config.getboolean('POS', 'OBJ_JJ_TO_NOUN')

parser = Parse(VERBOSE)
m = ManageFols(VERBOSE, LANGUAGE)



# Ontology creation procedures
class create_onto(Procedure): pass
class process_rule(Procedure): pass
class process_onto(Procedure): pass
class create_ent(Procedure): pass
class create_adj(Procedure): pass
class create_verb(Procedure): pass
class create_prep(Procedure): pass
class aggr_ent(Procedure): pass


# Reactive procedures - direct commands
class parse_command(Procedure): pass
class aggr_entities(Procedure): pass
class produce_intent(Procedure): pass
class produce_mod(Procedure): pass

# Reactive procedures - routines
class parse_routine(Procedure): pass
class produce_conds(Procedure): pass
class aggr_ent_conds(Procedure): pass
class produce_mod_conds(Procedure): pass
class produce_routine(Procedure): pass
class aggr_ent_rt(Procedure): pass
class produce_mod_rt(Procedure): pass

# check for routines execution
class check_conds(Procedure): pass

# start agent command
class go(Procedure): pass

# STT Front-End procedures
class s(Procedure): pass

# initialize Clauses Kb
class c(Procedure): pass

# mode reactors
class HOTWORD_DETECTED(Reactor): pass
class STT(Reactor): pass
class WAKE(Belief): pass
class LISTEN(Belief): pass
class REASON(Belief): pass
class RETRACT(Belief): pass
class IS_RULE(Belief): pass
class WAIT(Belief): pass
class ANSWER(Reactor): pass

# domotic reactive routines
class r1(Procedure): pass
class r2(Procedure): pass

# domotic direct commands
class d1(Procedure): pass
class d2(Procedure): pass

# domotic sensor simulatons
class s1(Procedure): pass
class s2(Procedure): pass

# Fol reasoning utterances
class c1(Procedure): pass
class c2(Procedure): pass
class c3(Procedure): pass
class c4(Procedure): pass
class c5(Procedure): pass
class c6(Procedure): pass

# Fol query utterance
class q(Procedure): pass

# normal requests beliefs
class GROUND(Belief): pass
class PRE_MOD(Belief): pass
class MOD(Belief): pass
class PRE_INTENT(Belief): pass
class INTENT(Reactor): pass

# routines beliefs
class PRE_ROUTINE(Belief): pass
class ROUTINE(Belief): pass
class ROUTINE_PRE_MOD(Belief): pass
class ROUTINE_MOD(Belief): pass
class ROUTINE_GROUND(Belief): pass

# conditionals beliefs
class PRE_COND(Belief): pass
class COND(Belief): pass
class COND_GROUND(Belief): pass
class COND_PRE_MOD(Belief): pass

class SENSOR(Belief): pass
class START_ROUTINE(Reactor): pass

# clause
class CLAUSE(Belief): pass
# action
class ACTION(Belief): pass
# preposition
class PREP(Belief): pass
# ground
class GND(Belief): pass
# adverb
class ADV(Belief): pass
# adjective
class ADJ(Belief): pass
# left clause
class LEFT_CLAUSE(Belief): pass
# definite clause
class DEF_CLAUSE(Belief): pass
# remain
class REMAIN(Belief): pass

# parse rule beliefs
class DEP(Belief): pass
class MST_ACT(Belief): pass
class MST_VAR(Belief): pass
class MST_PREP(Belief): pass
class MST_BIND(Belief): pass
class MST_COMP(Belief): pass
class MST_COND(Belief): pass
class parse_deps(Procedure): pass
class feed_mst(Procedure): pass
class PROCESS_STORED_MST(Reactor): pass



class log(Action):
    """log direct assertions from keyboard"""
    def execute(self, *args):
        a = str(args).split("'")

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\n"+a[1]+": "+a[5])


class beep(Action):
    """plays a beep"""
    def execute(self):
        winsound.PlaySound('ding.wav', winsound.SND_FILENAME)


class say(Action):
    """Text-to-Speech"""
    def execute(self, *args):
        text = args[0]()

        # setting TTS engine
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 150)

        engine.say(text)
        engine.runAndWait()


class reset_ct(Action):
    """Reset execution time"""
    def execute(self):
        parser.set_start_time()


class show_ct(Action):
    """Show execution time"""
    def execute(self):
        ct = parser.get_comp_time()
        print("\nExecution time: ", ct)

        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\nExecution time: "+str(ct))


class set_wait(Action):
    """Set duration of the session from WAIT_TIME in config.ini [AGENT]"""
    def execute(self):
        self.assert_belief(WAIT(WAIT_TIME))
        if LOG_ACTIVE:
            with open("log.txt", "a") as myfile:
                myfile.write("\n\n------ NEW SESSION ------ "+str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


class eval_cls(ActiveBelief):
    """ActiveBelief for Beliefs KB and Clauses KB interaction"""
    def evaluate(self, arg1, arg2, arg3):

        subj = str(arg1).split("'")[1]
        rel = str(arg2).split("'")[1]
        obj = str(arg3).split("'")[1]

        my_world = owlready2.World()
        my_world.get_ontology("west.owl").load()  # path to the owl file is given here

        graph = my_world.as_rdflib_graph()

        result = list(graph.query("ASK WHERE {<http://test/west.owl#"+subj+"> <http://www.w3.org/1999/02/22-rdf-syntax-ns#"+rel+"> <http://test/west.owl#"+obj+">.}"))
        print(result)

        return result[0]


class lemma_in_syn(ActiveBelief):
    """ActiveBelief for checking if a synset comprises a lemma"""
    def evaluate(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        synset = str(arg2).split("'")[1]

        pos = wordnet.VERB

        syns = wordnet.synsets(verb, pos=pos, lang=LANGUAGE)
        for syn in syns:
            if syn.name() == synset:
                return True
        return False


class preprocess_onto(Action):
    """Producting beliefs to feed the Definite Clauses Builder"""

    def execute(self, *args):
        type = str(args[0]())

        print("\n--------- NEW ONTOLOGY ---------\n ")
        print("type: " + type + "\n")

        self.MAIN_NEG_PRESENT = False

        deps = parser.get_last_deps()

        for i in range(len(deps)):
            governor = self.get_lemma(deps[i][1]).capitalize() + ":" + self.get_pos(deps[i][1])
            dependent = self.get_lemma(deps[i][2]).capitalize() + ":" + self.get_pos(deps[i][2])
            deps[i] = [deps[i][0], governor, dependent]

        print("\n" + str(deps))

        MST = parser.get_last_MST()
        print("\nMST: \n" + str(MST))
        print("\nGMC_SUPP: \n" + str(parser.GMC_SUPP))
        print("\nSUPP_SUPP_REV: \n" + str(parser.GMC_SUPP_REV))
        print("\nLCD: \n" + str(parser.LCD))


        # MST varlist correction on cases of adj-obj
        if OBJ_JJ_TO_NOUN is True:
            for v in MST[1]:
                if self.get_pos(v[1]) in ['JJ', 'JJR', 'JJS']:
                    old_value = v[1]
                    new_value = self.get_lemma(v[1]) + ":NNP"
                    v[1] = new_value

                    new_value_clean = parser.get_lemma(new_value.lower())[:-2]
                    print("\nadj-obj correction...", new_value_clean)

                    # checking if the lemma has a disambiguation
                    if new_value_clean in parser.GMC_SUPP_REV:
                        parser.LCD[parser.GMC_SUPP_REV[new_value_clean]] = new_value_clean

                    # binds correction
                    for b in MST[3]:
                        if b[0] == old_value:
                            b[0] = new_value


        vect_LR_fol = m.build_LR_fol(MST, 'e')

        print("\nBefore dealing case:\n" + str(vect_LR_fol))
        if len(vect_LR_fol) == 0:
            print("\n --- IMPROPER VERBAL PHRASE COSTITUTION ---")
            self.assert_belief(ANSWER("Improper verbal phrase"))
            return

        if type == "NOMINAL":
            # NOMINAL CASE
            CHECK_IMPLICATION = m.check_implication(vect_LR_fol)
            if not CHECK_IMPLICATION:
                if ASSIGN_RULES_ADMITTED:
                    check_isa = m.check_for_rule(deps, vect_LR_fol)
                    if check_isa:
                        self.assert_belief(IS_RULE("TRUE"))
                dclause = vect_LR_fol[:]
            else:
                dclause = vect_LR_fol[:]
                dclause[1] = ["==>"]
        else:
            # RULE CASE
            ent_root = self.get_ent_ROOT(deps)
            dav_rule = self.get_dav_rule(vect_LR_fol, ent_root)
            positive_vect_LR_fol = []
            for v in vect_LR_fol:
                lemma = self.get_lemma(v[0])[:-2]
                if self.check_neg(lemma, LANGUAGE) and v[1] == dav_rule:
                    self.assert_belief(RETRACT("ON"))
                else:
                    positive_vect_LR_fol.append(v)

            vect_LR_fol_plus_isa = m.build_isa_fol(positive_vect_LR_fol, deps)
            dclause = m.isa_fol_to_clause(vect_LR_fol_plus_isa)

        print("\nAfter dealing case:\n" + str(dclause))

        # IMPLICATION CASES
        if dclause[1][0] == "==>":

            print("\nPROCESSING LEFT HAND-SIDE...")
            self.process_fol(dclause[0], "LEFT")

            print("\nPROCESSING RIGHT HAND-SIDE...")
            self.process_fol(dclause[2], "RIGHT")

        # FLAT CASES
        else:
            nomain_negs = []
            # every verb/adj will carry its non-main negative
            negs = {}
            for n in nomain_negs:
                for v in dclause:
                    if v[1] == n[1]:
                        if v not in nomain_negs:
                            negs.update({v[0]: n[0]})

            self.process_fol(dclause, "FLAT")



    def get_ent_ROOT(self, deps):
        for d in deps:
            if d[0] == "ROOT":
                return d[1]

    def get_dav_rule(self, fol, ent_root):
        for f in fol:
            if f[0] == ent_root:
                return f[1]
        return False

    def check_neg(self, word, language):
        pos = wordnet.ADV
        syns = wordnet.synsets(word, pos=pos, lang=language)
        for synset in syns:
            if str(synset.name()) in ['no.r.01', 'no.r.02', 'no.r.03', 'not.r.01']:
                return True
        return False

    def get_nocount_lemma(self, lemma):
        lemma_nocount = ""
        total_lemma = lemma.split("_")

        for i in range(len(total_lemma)):
            if i == 0:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[1]
            else:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[1] + "_" + lemma_nocount
        return lemma_nocount

    def process_fol(self, vect_fol, id):

        # prepositions
        for v in vect_fol:
            if len(v) == 3:
                label = self.get_nocount_lemma(v[0])
                if id == "LEFT":
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")

                else:
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")


        # actions
        for v in vect_fol:
            if len(v) == 4:
                label = self.get_nocount_lemma(v[0])
                if INCLUDE_ACT_POS:
                    lemma = label
                else:
                    lemma = parser.get_lemma(label)

                self.assert_belief(ACTION(str(id), lemma, v[1], v[2], v[3]))
                print("ACTION(" + str(id) + ", " + lemma + ", " + v[1] + ", " + v[2] + ", " + v[3] + ")")


        # nouns
        for v in vect_fol:
            if len(v) == 2:
                if self.get_pos(v[0]) in ['NNP', 'NNPS', 'PRP', 'CD', 'NN', 'NNS', 'PRP', 'PRP$']:
                    label = self.get_nocount_lemma(v[0])
                    if INCLUDE_NOUNS_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(GND(str(id), v[1], lemma))
                    print("GND(" + str(id) + ", " + v[1] + ", " + lemma + ")")

        # adjectives, adverbs
        for v in vect_fol:
            if self.get_pos(v[0]) in ['JJ', 'JJR', 'JJS']:
                label = self.get_nocount_lemma(v[0])
                if id == "LEFT":
                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADJ(str(id), v[1], lemma))
                    print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                else:
                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADJ(str(id), v[1], lemma))
                    print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

            elif self.get_pos(v[0]) in ['RB', 'RBR', 'RBS', 'RP']:

                label = self.get_nocount_lemma(v[0])

                if id == "LEFT":
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADV(str(id), v[1], lemma))
                    print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                else:
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(ADV(str(id), v[1], lemma))
                    print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")



    def get_pos(self, s):
        first = s.split('_')[0]
        s_list = first.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class retract_clause(Action):
    """Retract a clause from the Clauses KB"""

    def execute(self, *args):
        sentence = args[0]()


class new_clause(Action):
    """Assert a clause in the Clauses KB"""

    def execute(self, *args):
        sentence = args[0]()


class reason(Action):
    """Query the Clauses KB with Backward-Chaining, and if it fails with Nested Reasoning"""

    def execute(self, *args):
        definite_clause = args[0]()


class assert_command(Action):
    """Producting beliefs to feed the Direct Command and Routine parsers"""

    def execute(self, *args):

        sentence = args[0]()

        # ----> words or chars not dealing well with fol conversion
        # verb_i2 must not be part of some verb_j1, with i!=j
        # [verb_i1, verb_i2]

        SWAP_STR = [["turn on", "change"], [":", "."], ["_", "-"]]

        for s in SWAP_STR:
            sentence = sentence.lower().replace(s[0], s[1])

        print(sentence)

        deps = parser.get_last_deps()
        MST = parser.get_last_MST()

        m = ManageFols(VERBOSE, LANGUAGE)
        vect_LR_fol = m.build_LR_fol(MST, 'd')

        # getting fol's type
        check_isa = False
        check_implication = m.check_implication(vect_LR_fol)
        if check_implication is False:
            check_isa = m.check_isa(vect_LR_fol, deps)

        gentle_LR_fol = m.vect_LR_to_gentle_LR(vect_LR_fol, deps, check_implication, check_isa)
        print(str(gentle_LR_fol))

        if len(vect_LR_fol) > 0 and vect_LR_fol[1][0] == "==>":

            dateTimeObj = datetime.now()
            id_routine = dateTimeObj.microsecond

            self.process_conditions(vect_LR_fol[0], id_routine)
            self.process_routine(vect_LR_fol[2], id_routine)
        else:
            self.process(vect_LR_fol)

    def process_conditions(self, vect_fol, id_routine):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond
        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(COND_PRE_MOD(g[1], lemma, g[2]))
        for g in vect_fol:
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(COND_GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
        for g in vect_fol:
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_COND(str(id_routine), verb, g[1], g[2], g[3]))

    def process_routine(self, vect_fol, id_routine):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond
        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(ROUTINE_PRE_MOD(g[1], lemma, g[2]))
        for g in vect_fol:
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(ROUTINE_GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
        for g in vect_fol:
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_ROUTINE(str(id_routine), verb, g[1], g[3], "", ""))

    def process(self, vect_fol):

        dateTimeObj = datetime.now()
        id_ground = dateTimeObj.microsecond

        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(PRE_MOD(g[1], lemma, g[2]))
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_INTENT(verb, g[1], g[3], "", ""))

    def get_verbs_nopos(self, lemma):
        lemma_nopos = ""
        total_lemma = lemma.split("_")

        for i in range(len(total_lemma)):
            if i == 0:
                lemma_nopos = total_lemma[i].split(':')[0][:-2]
            else:
                lemma_nopos = total_lemma[i].split(':')[0][:-2] + " " + lemma_nopos
        return lemma_nopos

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class join_grounds(Action):
    """join two GROUNDS Beliefs in one, with concatenated variables"""
    def execute(self, *args):
        dateTimeObj = datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class join_cond_grounds(Action):
    """join two COND_GROUNDS Beliefs in one, with concatenated variables"""
    def execute(self, *args):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(COND_GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class join_routine_grounds(Action):
    """join ROUTINE_GROUNDS Beliefs, with concatenated variables"""
    def execute(self, *args):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(ROUTINE_GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_intent_params(Action):
    """Append intent params considering a prepositions list"""

    def execute(self, *args):
        parameters_list = self.get_arg(str(args[6]))
        location = self.get_arg(str(args[5]))

        verb = self.get_arg(str(args[0]))
        dav = self.get_arg(str(args[1]))
        obj = self.get_arg(str(args[2]))

        prep = self.get_arg(str(args[3]))
        prep_obj = self.get_arg(str(args[4]))

        if prep in ["In"]:
            location = prep_obj
        else:

            if len(parameters_list) == 0:
                parameters_list = prep + " " + prep_obj
            else:
                parameters_list = parameters_list + ", " + prep + " " + prep_obj

        self.assert_belief(PRE_INTENT(verb, dav, obj, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_routine_params(Action):
    """Append routine params considering a prepositions list"""
    def execute(self, *args):

        id_routine = self.get_arg(str(args[0]))
        verb = self.get_arg(str(args[1]))
        dav = self.get_arg(str(args[2]))
        object_routine = self.get_arg(str(args[3]))

        prep = self.get_arg(str(args[4]))
        prep_obj = self.get_arg(str(args[5]))

        location = self.get_arg(str(args[6]))
        parameters_list = self.get_arg(str(args[7]))

        if prep in ["In"]:
            location = prep_obj
        else:
            if len(parameters_list) == 0:
                parameters_list = prep + " " + prep_obj
            else:
                parameters_list = parameters_list + ", " + prep + " " + prep_obj

        self.assert_belief(PRE_ROUTINE(id_routine, verb, dav, object_routine, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_intent_mods(Action):
    """Append intent modificators"""
    def execute(self, *args):

        verb = self.get_arg(str(args[0]))
        dav = self.get_arg(str(args[1]))
        object = self.get_arg(str(args[2]))

        mod = self.get_arg(str(args[3]))

        location = self.get_arg(str(args[4]))
        parameters_list = self.get_arg(str(args[5]))

        if len(parameters_list) == 0:
            parameters_list = mod
        else:
            parameters_list = parameters_list + ", " + mod

        self.assert_belief(PRE_INTENT(verb, dav, object, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_routine_mods(Action):
    """Append routine modificators"""
    def execute(self, *args):

        id_routine = self.get_arg(str(args[0]))
        verb = self.get_arg(str(args[1]))
        dav = self.get_arg(str(args[2]))
        object_routine = self.get_arg(str(args[3]))

        location = self.get_arg(str(args[5]))
        parameters_list = self.get_arg(str(args[6]))
        mod = self.get_arg(str(args[4]))

        if len(parameters_list) == 0:
            parameters_list = mod
        else:
            parameters_list = parameters_list + ", " + mod

        self.assert_belief(PRE_ROUTINE(id_routine, verb, dav, object_routine, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class exec_cmd(Action):
    """Simulating commands execution from the Smart Environment Interface"""
    def execute(self, *args):

        command = self.get_arg(str(args[0]))
        object = self.get_arg(str(args[1]))
        location = self.get_arg(str(args[2]))
        parameters = self.get_arg(str(args[3]))

        SWAP_STR = [[":", "."], ["_", "-"]]

        for s in SWAP_STR:
            object = object.replace(s[1], s[0])
            parameters = parameters.replace(s[1], s[0])

        print("\n---- Result: execution successful")
        print("\nAction: " + command)
        print("Object: " + object)

        if len(location) > 0:
            print("Location: " + location)

        if len(parameters) > 0:
            print("Parameters: " + parameters)
        print("\n")

    def get_arg(self, arg):
        s = arg.split("'")
        if len(s) == 3:
            return s[1]
        else:
            return s[3]


class simulate_sensor(Action):
    """Simulating Sensors behaviour for the Smart Environment Interface"""
    def execute(self, *args):
        verb = args[0]
        subject = args[1]
        object = args[2]
        print("\n\nasserting SENSOR(" + str(verb) + "," + str(subject) + "," + str(object) + ")...")
        self.assert_belief(SENSOR(verb, subject, object))



# ---------------------- Definite Clauses Builder section


class aggregate(Action):
    """join a couple of advectives (or adverbs) beliefs in one"""
    def execute(self, arg0, arg1, arg2, arg3, arg4):

        type = str(arg0).split("'")[1]
        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label1 = str(arg3).split("'")[3]
        label2 = str(arg4).split("'")[3]

        if len(label1.split('_')) > 1:
            conc_label = label1 + "_" + label2
        else:
            conc_label = label2 + "_" + label1

        if type == "ADJ":
            self.assert_belief(ADJ(id, var, conc_label))

        elif type == "ADV":
            self.assert_belief(ADV(id, var, conc_label))
        else:
            self.assert_belief(GND(id, var, conc_label))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]

    def get_pos(self, s):
        first = s.split('_')[0]
        s_list = first.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]


class merge(Action):
    """Merge a ground belief into a modificator argument"""
    def execute(self, arg1, arg2, arg3, arg4):
        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj = str(arg3).split("'")[3]
        noun = str(arg4).split("'")[3]

        new_label = adj + "(" + noun + ")"
        self.assert_belief(GND(id, var, new_label))


class ground_prep(Action):
    """Ground an object preposition belief"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        prep_label = str(arg3).split("'")[3]
        var_ground = str(arg4).split("'")[3]
        label_ground = str(arg5).split("'")[3]

        pn = self.get_par_number(label_ground)
        if pn == 0:
            new_object = label_ground + "(" + var_ground + ")"
        else:
            ls = label_ground.split(' ')
            if len(ls) > 1:
                new_object = label_ground
            else:
                new_object = label_ground[:-pn] + "(" + var_ground + ")"
                for i in range(pn):
                    new_object = new_object + ")"

        self.assert_belief(PREP(id, var, prep_label, new_object))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class int_preps_tognd(Action):
    """Merge two preposition belief in a ground beliefs"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):
        id = str(arg1).split("'")[3]
        var_ground_est = str(arg2).split("'")[3]
        var_ground_int = str(arg3).split("'")[3]
        prep_est_label = str(arg4).split("'")[3]
        prep_int_object = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        new_label = prep_est_label + "(" + ground_label + "(" + var_ground_est + "), " + prep_int_object + "(" + var_ground_int + "))"
        self.assert_belief(GND(id, var_ground_est, new_label))


class gprep_to_ground(Action):
    """Apply an object-grounded preposition belief to a ground belief"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        id = str(arg1).split("'")[3]
        var_prep_ground = str(arg2).split("'")[3]
        prep_label = str(arg3).split("'")[3]
        prep_object = str(arg4).split("'")[3]
        ground_label = str(arg5).split("'")[3]

        new_label = prep_label + "(" + ground_label + ", " + prep_object + ")"
        self.assert_belief(GND(id, var_prep_ground, new_label))


class adv_to_action(Action):
    """Apply an adverb to an action label"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):
        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        adv_label = str(arg6).split("'")[3]

        new_verb = adv_label + "(" + verb + ")"

        self.assert_belief(ACTION(id, new_verb, dav, subj, obj))


class act_to_clause(Action):
    """Turn a grounded action into a clause"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        pn = self.get_par_number(verb)
        if pn == 0:
            action = verb + "(" + subj + ", " + obj + ")"
        else:
            action = verb[:-pn] + "(" + subj + ", " + obj + ")"
            for i in range(pn):
                action = action + ")"

        self.assert_belief(CLAUSE(id, dav, action))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class ground_subj_act(Action):
    """Ground a subject action"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]

        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        pn_label = self.get_par_number(ground_label)
        t = ground_label.split(" ")

        if len(t) > 1:  # prep applied to ground case

            token1 = t[0][:-1]  # first token, without comma
            pn_token1 = self.get_par_number(token1)  # first token right-parentesys number

            if pn_token1 == 0:
                token1 = token1 + "(" + subj + ")"
            else:
                token1 = token1[:-pn_token1] + "(" + subj + ")"

            for i in range(pn_token1):
                token1 = token1 + ")"

            rem = ' '.join(t[1:])

            new_subj = token1 + ", " + rem[:-pn_label]

        else:
            if pn_label == 0:
                new_subj = ground_label + "(" + subj + ")"
            else:
                new_subj = ground_label[:-pn_label] + "(" + subj + ")"

        for i in range(pn_label):
            new_subj = new_subj + ")"

        self.assert_belief(ACTION(id, verb, dav, new_subj, obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class ground_obj_act(Action):
    """Ground an object action"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]

        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        pn_label = self.get_par_number(ground_label)

        t = ground_label.split(" ")
        if len(t) > 1:
            token1 = t[0][:-1]  # first token, without comma

            pn_token1 = self.get_par_number(token1)  # first token right-parentesys number

            if pn_token1 == 0:
                token1 = token1 + "(" + obj + ")"
            else:
                token1 = token1[:-pn_token1] + "(" + obj + ")"

            for i in range(pn_token1):
                token1 = token1 + ")"

            rem = ' '.join(t[1:])
            new_obj = token1 + ", " + rem[:-pn_label]

        else:
            if pn_label == 0:
                new_obj = ground_label + "(" + obj + ")"
            else:
                new_obj = ground_label[:-pn_label] + "(" + obj + ")"

        for i in range(pn_label):
            new_obj = new_obj + ")"

        self.assert_belief(ACTION(id, verb, dav, subj, new_obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class prep_to_clause(Action):
    """Applying a prep to a clause"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        id = str(arg1).split("'")[3]
        dav = str(arg2).split("'")[3]
        clause = str(arg3).split("'")[3]
        prep_label = str(arg4).split("'")[3]
        prep_obj = str(arg5).split("'")[3]

        new_clause = prep_label + "(" + clause + ", " + prep_obj + ")"

        self.assert_belief(CLAUSE(id, dav, new_clause))


class join_hand_sides(Action):
    """Join left and right hand sides into a definite clause"""
    def execute(self, arg1, arg2):
        lhs = str(arg1).split("'")[3]
        rhs = str(arg2).split("'")[3]

        new_clause = lhs + " ==> " + rhs
        self.assert_belief(DEF_CLAUSE(new_clause))


class conjunct_left_clauses(Action):
    """Joining left hand sides literals of a definite clause"""
    def execute(self, arg1, arg2):
        left_clause1 = str(arg1).split("'")[3]
        left_clause2 = str(arg2).split("'")[3]

        clauses_conjunction = left_clause1 + " & " + left_clause2
        self.assert_belief(LEFT_CLAUSE(clauses_conjunction))


class no_dav(ActiveBelief):
    """Check for davidsonian variable"""
    def evaluate(self, x):

        var = str(x).split("'")[3]
        # Check for davidsonian
        if var[0] == 'e' or var[0] == 'd':
            return False
        else:
            return True


class merge_act(Action):
    """Merge two actions into one via davidsonian variable"""
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        id = str(arg1).split("'")[3]

        verb_act_merged = str(arg2).split("'")[3]
        subj_act_merged = str(arg3).split("'")[3]
        obj_act_merged = str(arg4).split("'")[3]

        verb_act_merging = str(arg5).split("'")[3]
        dav_act_merging = str(arg6).split("'")[3]
        subj_act_merging = str(arg7).split("'")[3]

        pn_label = self.get_par_number(verb_act_merged)

        if pn_label > 0:
            new_obj = verb_act_merged[:-pn_label] + "(" + subj_act_merged + ", " + obj_act_merged + ")"
        else:
            new_obj = verb_act_merged + "(" + subj_act_merged + ", " + obj_act_merged + ")"

        for i in range(pn_label):
            new_obj = new_obj + ")"

        self.assert_belief(ACTION(id, verb_act_merging, dav_act_merging, subj_act_merging, new_obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


# ---------------------- Ontology creation Section



class aggrEntity(Action):
    """aggregate two entity beliefs in one"""
    def execute(self, arg1, arg2, arg3, arg4):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label1 = str(arg3).split("'")[3]
        label2 = str(arg4).split("'")[3]

        conc_label = label1 + "_" + label2
        self.assert_belief(GND(id, var, conc_label))



class createSubEntity(Action):
    """Creating a subclass of the class Entity"""
    def execute(self, arg):

        ent = str(arg).split("'")[3]
        print(ent)
        types.new_class(ent, (Entity,))


class createSubAdj(Action):
    """Creating a subclass of the class Adjective"""
    def execute(self, arg):

        ent = str(arg).split("'")[3]
        print(ent)
        types.new_class(ent, (Adjective,))


class createSubVerb(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg):

        ent = str(arg).split("'")[3]
        print(ent)

        types.new_class(ent, (Verb,))


class createSubPrep(Action):
    """Creating a subclass of the class Verb"""
    def execute(self, arg):

        ent = str(arg).split("'")[3]
        print(ent)

        types.new_class(ent, (Preposition,))


class saveOnto(Action):
    """Creating a subclass of the class Verb"""
    def execute(self):

        my_onto.save(file="west.owl", format="rdfxml")







# ---------------------- MST Builder Section

class parse_rules(Action):
    """Asserting dependencies related beliefs."""
    def execute(self, arg, dis):

        parser.flush()

        sent = str(arg).split("'")[3]
        if str(dis).split("'")[1] == "DISOK":
            DISOK = True
        else:
            DISOK = False

        print("\n", sent)
        deps = parser.get_deps(sent, True, DISOK)
        print("\n", deps)
        parser.set_last_deps(deps)

        for dep in deps:
            self.assert_belief(DEP(dep[0], str(dep[1]), str(dep[2])))


class create_MST_ACT(Action):
    """Asserting an MST  Action."""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        subj = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        subj_var = "x"+str(next(cnt))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, subj_var, obj_var))
        self.assert_belief(MST_VAR(subj_var, subj))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_ACT_PASS(Action):
    """Asserting an MST PASSIVE Action."""
    def execute(self, arg1, arg2):
        verb = str(arg1).split("'")[3]
        subj = str(arg2).split("'")[3]

        davidsonian = "e" + str(next(dav))
        subj_var = "x"+str(next(cnt))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, obj_var, subj_var))
        self.assert_belief(MST_VAR(subj_var, subj))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_PREP(Action):
    """Asserting an MST preposition."""
    def execute(self, arg1, arg2):
        dav = str(arg1).split("'")[3]
        prep = str(arg2).split("'")[3]

        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_PREP(prep, dav, obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class COND_WORD(ActiveBelief):
    """Checking for conditionals related words."""
    def evaluate(self, x):

        word = str(x).split("'")[3]
        # Check for conditional word
        if word.upper()[0:4] == "WHEN":
            return True
        else:
            return False


class NBW(ActiveBelief):
    """Checking for not blacklisted words."""
    def evaluate(self, x):

        word = str(x).split("'")[3]

        # Check for conditional word
        if self.get_lemma(word)[:-2].lower() not in ["that"]:
            return True
        else:
            return False

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class feed_mst_actions_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1, arg2, arg3, arg4):
        dav = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        subj = str(arg3).split("'")[3]
        obj = str(arg4).split("'")[3]

        action = []
        action.append(dav)
        action.append(verb)
        action.append(subj)
        action.append(obj)

        parser.feed_MST(action, 0)


class feed_mst_vars_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1, arg2):
        var = str(arg1).split("'")[3]
        val = str(arg2).split("'")[3]

        variable = []
        variable.append(var)
        variable.append(val)

        parser.feed_MST(variable, 1)


class feed_mst_preps_parser(Action):
    """Feed MST preps parser"""
    def execute(self, arg1, arg2, arg3):
        label = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        var_obj = str(arg3).split("'")[3]

        prep = []
        prep.append(label)
        prep.append(var)
        prep.append(var_obj)

        parser.feed_MST(prep, 2)


class feed_mst_binds_parser(Action):
    """Feed MST binds parser"""
    def execute(self, arg1, arg2):
        related = str(arg1).split("'")[3]
        relating = str(arg2).split("'")[3]

        bind = []
        bind.append(related)
        bind.append(relating)

        parser.feed_MST(bind, 3)


class feed_mst_comps_parser(Action):
    """Feed MST comps parser"""
    def execute(self, arg1, arg2):
        related = str(arg1).split("'")[3]
        relating = str(arg2).split("'")[3]

        comp = []
        comp.append(related)
        comp.append(relating)

        parser.feed_MST(comp, 4)


class feed_mst_conds_parser(Action):
    """Feed MST actions parser"""
    def execute(self, arg1):
        cond = str(arg1).split("'")[3]

        parser.feed_MST(cond, 5)


class flush_parser_cache(Action):
    """Flushing parser cache"""
    def execute(self):
        parser.flush()


class concat_mst_verbs(Action):
    """Concatenate composite verbs"""
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        verb1 = str(arg1).split("'")[3]
        verb2 = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        self.assert_belief(MST_ACT(verb1+"_"+verb2, dav, subj, obj))


class Past_Part(ActiveBelief):
    """Checking for Past Participle tense"""
    def evaluate(self, x):

        label = str(x).split("'")[3]

        if label.split(':')[1] == "VBN":
            return True
        else:
            return False


class Wh_Det(ActiveBelief):
    """Checking for Wh-determiner"""
    def evaluate(self, x):

        label = str(x).split("'")[3]

        if label != "?":
            if label.split(':')[1] == "WDT":
                return True
            else:
                return False
        else:
            return False


class create_MST_ACT_SUBJ(Action):
    """Asserting an MST Action with custom var subj"""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        subj_var = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, subj_var, obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_MST_ACT_EX(Action):
    """Asserting an MST Existencial"""
    def execute(self, arg1):

        verb = str(arg1).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x" + str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, "_", obj_var))
        self.assert_belief(MST_VAR(obj_var, "?"))


class create_IMP_MST_ACT(Action):
    """Asserting an Imperative MST Action."""
    def execute(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        obj = str(arg2).split("'")[3]

        davidsonian = "e"+str(next(dav))
        obj_var = "x"+str(next(cnt))

        self.assert_belief(MST_ACT(verb, davidsonian, "_", obj_var))
        self.assert_belief(MST_VAR(obj_var, obj))
