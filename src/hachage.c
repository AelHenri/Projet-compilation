#include <stdio.h>
#include <string.h>
#include "hachage.h"
#define SIZE 1013 

gen_t EMPTYH={"",0,"",""}; // un symbole vide
gen_t hachtab[SIZE];

int hachage(char *s) {
  unsigned int hash = 0; 
  while (*s!='\0') hash = hash*31 + *s++;
  return hash%SIZE;
}
gen_t findtab(char *s) {
  if (!strcmp(hachtab[hachage(s)].name,s)) return hachtab[hachage(s)];
  return EMPTYH;
}
void addtab(char *s,int type, char *varName) {
  gen_t *h=&hachtab[hachage(s)];
  h->name=s; h->type=type; h->code=NULL; h->var=varName;
}
void init() {
  int i;
  for (i=0; i<SIZE; i++) hachtab[i]=EMPTYH;
}