t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C).
t(_)::coauthor(A,B) :- researchtopic(A,C), \+researchtopic(B,C).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), affiliation(B,D).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), \+affiliation(B,D).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), affiliation(B,E), location(D,F), location(E,F).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), affiliation(B,E), location(D,F), \+location(E,F).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), affiliation(B,E), institutetype(D,F), institutetype(E,F).
t(_)::coauthor(A,B) :- researchtopic(A,C), researchtopic(B,C), affiliation(A,D), affiliation(B,E), institutetype(D,F), \+institutetype(E,F).
t(_)::coauthor(A,B).