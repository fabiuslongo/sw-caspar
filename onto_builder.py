from phidias.Lib import *
from actions import *



# ONTOLOGY BUILDER

process_onto() >> [create_ent(), create_adj()]

"""
parse() >> [aggr_adj(), aggr_adv(), aggr_nouns(), mod_to_gnd(), gnd_prep_obj(), prep_to_gnd(), gnd_actions(), apply_adv(), actions_to_clauses(), finalize_gnd()]
# aggregate adjectives
aggr_adj() / (ADJ(I, X, L) & ADV(I, X, M)) >> [show_line("\naggregating adj-adv: ", L," - ", M), -ADJ(I, X, L), -ADV(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / (ADJ(I, X, L) & ADJ(I, X, M) & neq(L, M)) >> [show_line("\naggregating adjectives: ", L," - ", M), -ADJ(I, X, L), -ADJ(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / ADJ(I, X, L) >> [show_line("\nAdjectives aggregation done")]
"""

create_ent() / GND("FLAT", X, Y) >> [show_line("\ncreating entity: ", Y), -GND("FLAT", X, Y), createSubEntity(Y), create_ent()]
create_ent() >> [show_line("\nentity creation done")]

create_adj() / ADJ("FLAT", X, Y) >> [show_line("\ncreating adjective: ", Y), -ADJ("FLAT", X, Y), createSubAdj(Y), create_adj()]
create_adj() >> [show_line("\nadjective creation done")]



