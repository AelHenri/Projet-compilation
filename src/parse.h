#include <stdio.h>
#include <stdlib.h>

#ifndef _PARSE_H_
#define _PARSE_H_

enum base {INT_T=0, FLOAT_T, ARRAY_T};

typedef struct gen_t {
	char *code;
	int type;
	char *name;
}gen_t;

#endif