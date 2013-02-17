
all: ex_1_1.rkt ex_1_2.rkt

ex_1_1.rkt: repl_to_rkt.py Makefile ex_1_1.repl
	python repl_to_rkt.py ex_1_1.repl > ex_1_1.rkt
	racket ex_1_1.rkt

ex_1_2.rkt: repl_to_rkt.py Makefile ex_1_2.repl
	python repl_to_rkt.py ex_1_2.repl > ex_1_2.rkt
	racket ex_1_2.rkt
