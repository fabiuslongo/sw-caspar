from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() >> [aggr_ent(), create_ent(), create_adj(), create_verb(), saveOnto()]

"""
parse() >> [aggr_adj(), aggr_adv(), aggr_nouns(), mod_to_gnd(), gnd_prep_obj(), prep_to_gnd(), gnd_actions(), apply_adv(), actions_to_clauses(), finalize_gnd()]
# aggregate adjectives
aggr_adj() / (ADJ(I, X, L) & ADV(I, X, M)) >> [show_line("\naggregating adj-adv: ", L," - ", M), -ADJ(I, X, L), -ADV(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / (ADJ(I, X, L) & ADJ(I, X, M) & neq(L, M)) >> [show_line("\naggregating adjectives: ", L," - ", M), -ADJ(I, X, L), -ADJ(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / ADJ(I, X, L) >> [show_line("\nAdjectives aggregation done")]
"""

aggr_ent() / (GND(X, Y, Z) & GND(X, Y, K) & neq(Z, K)) >> [show_line("\naggregating entity: ", Y), -GND(X, Y, Z), -GND(X, Y, K), aggrEntity(X, Y, Z, K), aggr_ent()]
aggr_ent() >> [show_line("\nentities aggregation done.")]

create_ent() / GND("FLAT", X, Y) >> [show_line("\ncreating entity: ", Y), -GND("FLAT", X, Y), createSubEntity(Y), create_ent()]
create_ent() >> [show_line("\nentity creation done.")]

create_adj() / ADJ("FLAT", X, Y) >> [show_line("\ncreating adjective: ", Y), -ADJ("FLAT", X, Y), createSubAdj(Y), create_adj()]
create_adj() >> [show_line("\nadjective creation done.")]

create_verb() / ACTION("FLAT", X, Y, Z, W) >> [show_line("\ncreating verb: ", X), -ACTION("FLAT", X, Y, Z, W), createSubVerb(X), create_verb()]
create_verb() >> [show_line("\nverb creation done.")]




