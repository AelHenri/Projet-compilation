#include <stdio.h>
#include <stdlib.h>

#ifndef _PARSE_H_
#define _PARSE_H_

enum base {VOID_T, INT_T=0, FLOAT_T, ARRAY_T};

typedef struct gen_t {
	char *code;
	int type;
	char *var;
}gen_t;

#endif