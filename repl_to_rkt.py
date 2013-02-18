#!/usr/bin/env python
import sys

ST_COMMENT = 1
ST_QUESTION = 2
ST_ANSWER = 3

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
                print '(check-expect\n\t ' , '\n\t\t'.join(q_acc)
                print '\t ', '\n\t'.join(a_acc), ' )'
                q_acc = []; a_acc = []
                state = ST_COMMENT

        if line and state == ST_QUESTION:
            if line[0] in ">#%":
                print '\n'.join(l[1:] if l[0] == ' ' else l for l in q_acc)
                state = ST_COMMENT
                q_acc = []
            elif line[0] in (" ", "\t"):
                q_acc.append( line )
            else:
                state = ST_ANSWER
                a_acc.append( line )

        if line and state == ST_COMMENT:
            if line[0] == '>':
                state = ST_QUESTION
                q_acc.append( line[1:] )
        if state in (ST_COMMENT, ST_QUESTION, ST_ANSWER):
            print ';; ',
        print line.rstrip()


if state == ST_QUESTION:
    print '\n'.join(l.lstrip() for l in q_acc)
elif state == ST_ANSWER:
    print '(check-expect\n\t ' , '\n\t\t'.join(q_acc)
    print '\t ', '\n\t'.join(a_acc), ' )'

print "(test)"
