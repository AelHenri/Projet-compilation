LEX=lex
YACC=bison
CFLAGS=-Wall -D_GNU_SOURCE
CC=gcc

all:parse

parse:grammar.c scanner.c hachage.c
	$(CC) $(CFLAGS) -o $@ $^

grammar.c:grammar.y
	$(YACC) -d -o $@ --defines=grammar.tab.h $^

%.c:%.l
	$(LEX) -o $@ $^

clean:
	rm -f grammar.c scanner.c
