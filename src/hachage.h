#ifndef _HACHAGE_H_
#define _HACHAGE_H_

#include <stdio.h>
#include <string.h>

enum base {VOID_T, INT_T=0, FLOAT_T, ARRAY_T};

typedef struct {
  char *name;
  int type;
  char *code;
  char *var;
} gen_t;

int hachage(char *s);
gen_t findtab(char *s);
void addtab(char *s,int type, char* varName);
void init();

#endif