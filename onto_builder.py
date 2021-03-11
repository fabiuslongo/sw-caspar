from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() / ID(I) >> [aggr_ent(), create_verb(), create_adj(), create_ent(), create_prep(), saveOnto(), create_rule(), -ID(I)]




aggr_ent() / (GND(X, Y, Z) & GND(X, Y, K) & neq(Z, K)) >> [show_line("\naggregating entity: ", Y), -GND(X, Y, Z), -GND(X, Y, K), aggrEntity(X, Y, Z, K), aggr_ent()]
aggr_ent() >> [show_line("\nentities aggregation done.")]


create_adj() / (ADJ("FLAT", X, Y) & GND("FLAT", X, S) & ID(I)) >> [show_line("\ncreating entity+adjective: ", Y), -ADJ("FLAT", X, Y), applyAdj(I, Y, S), create_adj()]
create_adj() >> [show_line("\nadjective creation done.")]

create_ent() / (GND("FLAT", X, Y) & ID(I)) >> [show_line("\ncreating entity: ", Y), -GND("FLAT", X, Y), createSubEntity(I, Y), create_ent()]
create_ent() >> [show_line("\nentity creation done.")]

create_prep() / PREP("FLAT", X, Y, Z) >> [show_line("\ncreating prep: ", Y), -PREP("FLAT", X, Y, Z), createSubPrep(Y), create_prep()]
create_prep() >> [show_line("\nprep creation done.")]


create_verb() / (ACTION("FLAT", V, D, X, Y) & GND("FLAT", X, K) & GND("FLAT", Y, J) & ID(I)) >> [show_line("\ncreating verb: ", V), -ACTION("FLAT", V, D, X, Y), createSubVerb(I, V, K, J), create_verb()]
create_verb() >> [show_line("\nverb creation done.")]

create_rule() / (ACTION("LEFT", V, E, X, Y) & RULE(R)) >> [show_line("\nupdating rule: ", V), -ACTION("LEFT", V, E, X, Y), create_rule()]
create_rule() / RULE(R) >> [show_line("\nrule update completed."), -RULE(R)]





