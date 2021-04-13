from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() / ID(I) >> [aggr_ent(), create_adv(), create_gnd_prep(), create_prep(), create_verb(), create_head(), create_body(), finalize_rule(), create_ner(), saveOnto(), -ID(I)]

# Grounds aggregation
aggr_ent() / (GND(X, Y, Z) & GND(X, Y, K) & neq(Z, K)) >> [show_line("\naggregating entity: ", Y), -GND(X, Y, Z), -GND(X, Y, K), aggrEntity(X, Y, Z, K), aggr_ent()]
aggr_ent() >> [show_line("\nentities aggregation done.")]

# Adverb productions
create_adv() / (ACTION("FLAT", V, D, X, Y) & ADV("FLAT", D, K) & ID(I)) >> [show_line("\ncreating adverbs: ", Y), -ADV("FLAT", D, K), applyAdv(I, V, K), create_adv()]
create_adv() / (ACTION("ROOT", "FLAT", V, D, X, Y) & ADV("FLAT", D, K) & ID(I)) >> [show_line("\ncreating adverbs (ROOT): ", Y), -ADV("FLAT", D, K), applyAdv(I, V, K), create_adv()]
create_adv() >> [show_line("\nadverb creation done.")]

# Verb-related prepositions
create_prep() / (ACTION("FLAT", V, D, X, Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating verb related prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPrep(I, V, K, S), create_prep()]
create_prep() / (ACTION("ROOT", "FLAT", V, D, X, Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating verb related prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPrep(I, V, K, S), create_prep()]
create_prep() >> [show_line("\nverv related prep creation done.")]

# Ground-related Prepositions
create_gnd_prep() / (GND("FLAT", X, K) & PREP("FLAT", X, Y, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating gnd related prep: ", Y), -PREP("FLAT", X, Y, Z), -GND("FLAT", Z, S), createSubGndPrep(I, K, Y, S), create_prep()]
create_gnd_prep() >> [show_line("\ngnd related prep creation done.")]

# Ordinary verbs production
create_verb() / (GND("FLAT", X, K) & ADJ("FLAT", X, J)) >> [show_line("\ncreating adjective: ", J), -ADJ("FLAT", X, J), createAdj(K, J), create_verb()]

create_verb() / (ACTION("ROOT", "FLAT", "Be:VBZ", D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\nVERB+Ass.Rule (VBZ)"), -ACTION("ROOT", "FLAT", "Be:VBZ", D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubCustVerb(I, "Be:VBZ", K, J), createAssRule(K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", "Be:VBP", D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\nVERB+Ass.Rule (VBP)"), -ACTION("ROOT", "FLAT", "Be:VBP", D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubCustVerb(I, "Be:VBP", K, J), createAssRule(K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", "Be:VBZ", D, X, Y) & GND("FLAT", X, K) & ADJ("FLAT", Y, J) & ID(I)) >> [show_line("\nVERB+Ass.Rule ADJ (VBZ)"), -ACTION("ROOT", "FLAT", "Be:VBZ", D, X, Y), -GND("FLAT", X, K), -ADJ("FLAT", Y, J), createSubCustVerb(I, "Be:VBZ", K, J), createAdj(K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", "Be:VBP", D, X, Y) & GND("FLAT", X, K) & ADJ("FLAT", Y, J) & ID(I)) >> [show_line("\nVERB+Ass.Rule ADJ (VBP)"), -ACTION("ROOT", "FLAT", "Be:VBP", D, X, Y), -GND("FLAT", X, K), -ADJ("FLAT", Y, J), createSubCustVerb(I, "Be:VBP", K, J), createAdj(K, J), create_verb()]

create_verb() / (ACTION("FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating normal verb: ", V), -ACTION("FLAT", V, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubVerb(I, V, K, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating normal verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubVerb(I, V, K, J), create_verb()]

create_verb() / (ACTION("FLAT", V, D, "__", Y) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating passive verb: ", V), -ACTION("FLAT", V, D, "__", Y), -GND("FLAT", Y, J), createPassSubVerb(I, V, J), create_verb()]
create_verb() / (ACTION("FLAT", V, D, X, "__") & GND("FLAT", X, K) & ID(I)) >> [show_line("\ncreating intransitive verb: ", V), -ACTION("FLAT", V, D, X, "__"), -GND("FLAT", X, K), createIntrSubVerb(I, V, K), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, "__", Y) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating passive verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, "__", Y), -GND("FLAT", Y, J), createPassSubVerb(I, V, J), create_verb()]
create_verb() / (ACTION("ROOT", "FLAT", V, D, X, "__") & GND("FLAT", X, K) & ID(I)) >> [show_line("\ncreating intransitive verb (ROOT): ", V), -ACTION("ROOT", "FLAT", V, D, X, "__"), -GND("FLAT", X, K), createIntrSubVerb(I, V, K), create_verb()]

create_verb() >> [show_line("\nverb creation done.")]

# Named Entity Recognition production
create_ner() / (NER("GPE", Y) & ID(I)) >> [show_line("\nCreating GPE NER: ", Y), -NER("GPE", Y), createPlace(I, Y), create_ner()]
create_ner() / (NER("DATE", Y) & ID(I)) >> [show_line("\nCreating DATE NER: ", Y), -NER("DATE", Y), createDate(I, Y), create_ner()]
create_ner() / (NER(X, Y) & ID(I)) >> [-NER(X, Y), create_ner()]
create_ner() / ID(I) >> [show_line("\nNER creation done.")]


#  COPULAR VERBS IMPLICATIONS

# updating head/absorbing copular verb
create_head() / (ACTION("RIGHT", "Be:VBZ", E, X, Y) & GND("RIGHT", X, K) & GND("RIGHT", Y, V) & RULE(R)) >> [show_line("\nupdating implication head: ", V), -ACTION("RIGHT", "Be:VBZ", E, X, Y), -GND("RIGHT", X, K), -GND("RIGHT", Y, V), +SUBJ(Y, K), -RULE(R), fillGndRule("RIGHT", R, Y, V), create_head()]
create_head() / ACTION("RIGHT", V, E, X, Y) >> [show_line("\nnon-copular verb not admitted for head: ", V), -ACTION("RIGHT", V, E, X, Y), create_head()]
create_head() / (ACTION("ROOT", "RIGHT", "Be:VBZ", E, X, Y) & GND("RIGHT", X, K) & GND("RIGHT", Y, V) & RULE(R)) >> [show_line("\nupdating implication head (ROOT): ", V), -ACTION("ROOT", "RIGHT", "Be:VBZ", E, X, Y), -GND("RIGHT", X, K), -GND("RIGHT", Y, V), +SUBJ(Y, K), -RULE(R), fillGndRule("RIGHT", R, Y, V), create_head()]
create_head() / ACTION("ROOT", "RIGHT", V, E, X, Y) >> [show_line("\nnon-copular verb not admitted for head (ROOT): ", V), -ACTION("ROOT", "RIGHT", V, E, X, Y), create_head()]

create_head() / GND("RIGHT", X, K) >> [show_line("\ngnd linked to non-copular verbs not admitted for head: ", K), -GND("RIGHT", X, K), create_head()]
create_head() / PREP("RIGHT", E, X, Y) >> [show_line("\npreps not admitted for head: ", X), -PREP("RIGHT", E, X, Y), create_head()]
create_head() / ADJ("RIGHT", X, K) >> [show_line("\nadjectives not admitted for head: ", K), -ADJ("RIGHT", X, K), create_head()]
create_head() / ADV("RIGHT", D, K) >> [show_line("\nadverbs not admitted for head: ", K), -ADV("RIGHT", D, K), create_head()]
create_head() / RULE(R) >> [show_line("\nhead creation completed")]

create_body() / (ACTION("LEFT", V, D, "__", Y) & RULE(R)) >> [show_line("\nupdating body with passive verb: ", V), -ACTION("LEFT", V, D, "__", Y), -RULE(R), fillPassActRule(R, V, D, Y), create_body()]
create_body() / (ACTION("LEFT", V, D, X, "__") & RULE(R)) >> [show_line("\nupdating body with intransitive verb: ", V), -ACTION("LEFT", V, D, X, "__"), -RULE(R), fillIntraActRule(R, V, D, X), create_body()]
create_body() / (ACTION("LEFT", V, E, X, Y) & RULE(R)) >> [show_line("\nupdating body with normal verb: ", V), -ACTION("LEFT", V, E, X, Y), -RULE(R), fillActRule(R, V, E, X, Y), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, D, "__", Y) & RULE(R)) >> [show_line("\nupdating body with passive verb (ROOT): ", V), -ACTION("ROOT","LEFT", V, D, "__", Y), -RULE(R), fillPassActRule(R, V, D, Y), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, D, X, "__") & RULE(R)) >> [show_line("\nupdating body with intransitive verb (ROOT): ", V), -ACTION("ROOT", "LEFT", V, D, X, "__"), -RULE(R), fillIntraActRule(R, V, D, X), create_body()]
create_body() / (ACTION("ROOT", "LEFT", V, E, X, Y) & RULE(R)) >> [show_line("\nupdating body with normal verb (ROOT): ", V), -ACTION("ROOT","LEFT", V, E, X, Y), -RULE(R), fillActRule(R, V, E, X, Y), create_body()]

# updating body with adjectives
create_body() / (ADJ("LEFT", X, K) & RULE(R)) >> [show_line("\nupdating body with adj: ", K), -ADJ("LEFT", X, K), -RULE(R), fillAdjRule(R, X, K), create_body()]

# updating body with adverbs
create_body() / (ADV("LEFT", D, K) & RULE(R)) >> [show_line("\nupdating body with adj: ", K), -ADV("LEFT", D, K), -RULE(R), fillAdjRule(R, D, K), create_body()]

#updating body with prepositions
create_body() / (PREP("LEFT", E, X, Y) & RULE(R)) >> [show_line("\nupdating body with prep: ", X), -RULE(R), -PREP("LEFT", E, X, Y), fillPrepRule("LEFT", R, E, X, Y), create_body()]

# updating body with grounds
create_body() / (GND("LEFT", X, Y) & RULE(R) & SUBJ(Z, Y)) >> [show_line("\nupdating body with gnd: ", Y), -GND("LEFT", X, Y), -RULE(R), fillGndRule("LEFT", R, Z, Y), create_body()]
create_body() / (GND("LEFT", X, Y) & RULE(R)) >> [show_line("\nupdating body with gnd: ", Y), -GND("LEFT", X, Y), -RULE(R), fillGndRule("LEFT", R, X, Y), create_body()]
create_body() / (RULE(R) & SUBJ(X, Y)) >> [show_line("\nupdating body with gnd completed."),  -SUBJ(X, Y)]

finalize_rule() / (RULE(R) & WFR(R)) >> [show_line("\nfinalizing well formed rule..."), -RULE(R), declareRule(R)]
finalize_rule() / RULE(R) >> [show_line("\nthe rule is not well formed!"), -RULE(R)]






