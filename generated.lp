activity(a).
has_attribute(a, grade).
activity(b).
has_attribute(b, grade).

value(grade, 1..5).

template(0,"Response").
activation(0,a).
activation_condition(0,T):- activation_condition_1(0,T).
activation_condition_1(0,T) :- assigned_value(grade,V,T),V=3.

target(0,b).
correlation_condition(0,T):- correlation_condition_1(0,T).
correlation_condition_1(0,T) :- assigned_value(grade,V,T),V>5.