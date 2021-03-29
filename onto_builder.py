from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() / ID(I) >> [aggr_ent(), create_adj(), create_adv(), create_gnd_prep(), create_prep(), create_verb(), create_body(), create_head(), finalize_rule(), saveOnto(), -ID(I)]


# flats

aggr_ent() / (GND(X, Y, Z) & GND(X, Y, K) & neq(Z, K)) >> [show_line("\naggregating entity: ", Y), -GND(X, Y, Z), -GND(X, Y, K), aggrEntity(X, Y, Z, K), aggr_ent()]
aggr_ent() >> [show_line("\nentities aggregation done.")]

create_adj() / (ADJ("FLAT", X, Y) & GND("FLAT", X, S) & ID(I)) >> [show_line("\ncreating entity+adjective: ", Y), -ADJ("FLAT", X, Y), applyAdj(I, Y, S), create_adj()]
create_adj() >> [show_line("\nadjective creation done.")]

create_adv() / (ACTION("FLAT", V, D, X, Y) & ADV("FLAT", D, K) & ID(I)) >> [show_line("\ncreating adverbs: ", Y), -ADV("FLAT", D, K), applyAdv(I, V, K), create_adv()]
create_adv() >> [show_line("\nadverb creation done.")]

create_prep() / (ACTION("FLAT", V, D, X, Y) & PREP("FLAT", D, K, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating verb prep: ", K), -PREP("FLAT", D, K, Z), -GND("FLAT", Z, S), createSubPrep(I, V, K, S), create_prep()]
create_prep() >> [show_line("\nprep creation done.")]

create_gnd_prep() / (GND("FLAT", X, K) & PREP("FLAT", X, Y, Z) & GND("FLAT", Z, S) & ID(I)) >> [show_line("\ncreating gnd prep: ", Y), -PREP("FLAT", X, Y, Z), -GND("FLAT", Z, S), createSubGndPrep(I, K, Y, S), create_prep()]
create_gnd_prep() >> [show_line("\nprep creation done.")]

create_verb() / (ACTION("FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating normal verb: ", V), -ACTION("FLAT", V, D, X, Y), -GND("FLAT", X, K), -GND("FLAT", Y, J), createSubVerb(I, V, K, J), create_verb()]
create_verb() / (ACTION("FLAT", V, D, "__", Y) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating passive verb: ", V), -ACTION("FLAT", V, D, "__", Y), -GND("FLAT", Y, J), createPassSubVerb(I, V, J), create_verb()]
create_verb() / (ACTION("FLAT", V, D, X, "__") & GND("FLAT", X, K) & ID(I)) >> [show_line("\ncreating intransitive verb: ", V), -ACTION("FLAT", V, D, X, "__"), -GND("FLAT", X, K), createIntrSubVerb(I, V, K), create_verb()]

create_verb() >> [show_line("\nverb creation done.")]


# implications

create_body() / (ACTION("LEFT", V, E, X, Y) & RULE(R)) >> [show_line("\nupdating body with action: ", V), -ACTION("LEFT", V, E, X, Y), -RULE(R), +SUBJ(X), fillActRule("LEFT", R, V, E, X, Y), create_body()]

create_body() / (GND("LEFT", X, Y) & RULE(R) & SUBJ(X)) >> [show_line("\nupdating body with gnd: ", Y), -GND("LEFT", X, Y), -RULE(R), -SUBJ(X), +SUBJ(X, Y), fillGndRule("LEFT", R, X, Y), create_body()]
create_body() / (GND("LEFT", X, Y) & RULE(R)) >> [show_line("\nupdating body with gnd: ", Y), -GND("LEFT", X, Y), -RULE(R), fillGndRule("LEFT", R, X, Y), create_body()]

create_body() / (ADJ("LEFT", X, Y) & RULE(R)) >> [show_line("\nupdating body with adj: ", Y), -ADJ("LEFT", X, Y), -RULE(R), fillAdjRule("LEFT", R, X, Y), create_body()]
create_body() / (PREP("LEFT", E, X, Y) & RULE(R)) >> [show_line("\nupdating body with prep: ", X), -RULE(R), -PREP("LEFT", E, X, Y), fillPrepRule("LEFT", R, E, X, Y), create_body()]

create_head() / (ACTION("RIGHT", "Be:VBZ", E, X, Y) & GND("RIGHT", X, K) & GND("RIGHT", Y, V) & SUBJ(S, K) & RULE(R)) >> [show_line("\nupdating implication head: ", V), -ACTION("RIGHT", "Be:VBZ", E, X, Y), -GND("RIGHT", X, K), -GND("RIGHT", Y, V), -SUBJ(S, K), -RULE(R), fillGndRule("RIGHT", R, S, V), create_head()]
create_head() / (GND("RIGHT", X, K) & RULE(R)) >> [show_line("\nupdating isa head with gnd: ", K), -GND("RIGHT", X, K), -RULE(R), fillGndRule("RIGHT", R, X, K), create_head()]
create_head() / (ADJ("RIGHT", X, K) & RULE(R)) >> [show_line("\nupdating isa head with adj: ", K), -ADJ("RIGHT", X, K), -RULE(R), fillAdjRule("RIGHT", R, X, K), create_head()]


finalize_rule() / (RULE(R) & WFR(R)) >> [show_line("\nfinalizing well formed rule..."), -RULE(R), declareRule(R)]
finalize_rule() / RULE(R) >> [show_line("\nthe rule is not well formed!"), -RULE(R), declareRule(R)]






