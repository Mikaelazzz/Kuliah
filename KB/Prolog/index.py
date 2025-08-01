# -*- coding: utf-8 -*-
"""Tugas Prolog.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qX5DYTxDrJAB7uS8_upW3zCPHphW0S3C

# Tugas Prolog
Vincentius Johanes Lwie Jaya / 233408010
"""

!apt-get update
!apt-get install -y swi-prolog

# Commented out IPython magic to ensure Python compatibility.
# %%file animal.pro
# 
# go :- hypothesize(Animal),
#       write('I guess that the animal is: '),
#       write(Animal),
#       nl,
#       undo.
# 
# /* hypotheses to be tested */
# hypothesize(tiger)     :- tiger, !.
# hypothesize(zebra)     :- zebra, !.
# hypothesize(ostrich)   :- ostrich, !.
# hypothesize(penguin)   :- penguin, !.
# hypothesize(eagle)     :- eagle, !.
# hypothesize(fox)       :- fox, !.
# hypothesize(dolphin)   :- dolphin, !.
# hypothesize(unknown).             /* no diagnosis */
# 
# /* animal identification rules */
# tiger :- mammal,
#          carnivore,
#          verify(has_tawny_color),
#          verify(has_black_stripes).
# 
# zebra :- ungulate,
#          verify(has_black_stripes).
# 
# ostrich :- bird,
#            verify(does_not_fly),
#            verify(has_long_neck).
# 
# penguin :- bird,
#            verify(does_not_fly),
#            verify(swims),
#            verify(is_black_and_white).
# 
# eagle :- bird,
#          verify(flys_well),
#          verify(hunts_prey).
# 
# fox :- mammal,
#         carnivore,
#         verify(has_red_fur),
#         verify(lives_on_land),
#         verify(gives_milk).
# 
# dolphin :- mammal,
#             verify(lives_in_water),
#             verify(swims),
#             verify(does_not_fly).
# 
# /* classification rules */
# mammal    :- verify(has_hair), !.
# mammal    :- verify(gives_milk).
# bird      :- verify(has_feathers), !.
# bird      :- verify(flys),
#              verify(lays_eggs).
# carnivore :- verify(eats_meat), !.
# carnivore :- verify(has_pointed_teeth),
#              verify(has_claws),
#              verify(has_forward_eyes).
# ungulate :- mammal,
#             verify(has_hooves), !.
# ungulate :- mammal,
#             verify(chews_cud).
# 
# /* how to ask questions */
# ask(Question) :-
#     write('Does the animal have the following attribute: '),
#     write(Question),
#     write('? '),
#     read(Response),
#     nl,
#     ( (Response == yes ; Response == y)
#       ->
#        assert(yes(Question)) ;
#        assert(no(Question)), fail).
# 
# :- dynamic yes/1,no/1.
# 
# /* How to verify something */
# verify(S) :-
#    (yes(S)
#     ->
#     true ;
#     (no(S)
#      ->
#      fail ;
#      ask(S))).
# 
# /* undo all yes/no assertions */
# undo :- retract(yes(_)),fail.
# undo :- retract(no(_)),fail.
# undo.

!swipl -s animal.pro -g "go,halt"