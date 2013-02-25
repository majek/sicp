#!/usr/bin/env python
import sys

ST_COMMENT = 1
ST_QUESTION = 2
ST_ANSWER = 3

FL_EXACT = 'e'
FL_FLOAT = 'f'

def do_print(q_acc, a_acc, flavour):
    if flavour == FL_EXACT:
        print '(check-expect\n\t ' , '\n\t\t'.join(q_acc)
        print '\t ', '\n\t'.join(a_acc),
        print ' )'
    if flavour == FL_FLOAT:
        print '(check-within\n\t ' , '\n\t\t'.join(q_acc)
        print '\t ', '\n\t'.join(a_acc),
        print ' 0.00000001 )'
    while q_acc:
        q_acc.pop()
    while a_acc:
        a_acc.pop(0)

state = ST_COMMENT
q_acc = []
a_acc = []
print "#lang racket"
print "(require test-engine/racket-tests)"
with open(sys.argv[1], 'rb') as fd:
    while True:
        line = fd.readline()
        if not line:
            break
        line = line.rstrip()

        if line and state == ST_ANSWER:
            if line[0] in (" ", "\t"):
                a_acc.append( line )
            else:
                do_print(q_acc, a_acc, flavour)
                state = ST_COMMENT

        if line and state == ST_QUESTION:
            if line[0] in ">#%" or line[0:2] in (".>"):
                print '\n'.join(l[1:] if l[0] == ' ' else l for l in q_acc)
                state = ST_COMMENT
                q_acc = []
            elif line[0] in (" ", "\t"):
                q_acc.append( line )
            else:
                state = ST_ANSWER
                a_acc.append( line )

        if line and state == ST_COMMENT:
            if line[0:2] == '> ':
                state = ST_QUESTION
                flavour = FL_EXACT
                q_acc.append( line[1:] )
            elif line[0:3] == '.> ':
                state = ST_QUESTION
                flavour = FL_FLOAT
                q_acc.append( line[2:] )
        if state in (ST_COMMENT, ST_QUESTION, ST_ANSWER):
            print ';; ',
        print line.rstrip()


if state == ST_QUESTION:
    print '\n'.join(l.lstrip() for l in q_acc)
elif state == ST_ANSWER:
    do_print(q_acc, a_acc, flavour)

print "(test)"
