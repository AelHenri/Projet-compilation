#include <stdio.h>
#include <stdlib.h>

#ifndef _TYPES_H_
#define _TYPES_H_

enum base {INT_T, FLOAT_T, ARRAY_T};

struct typeName {
	enum base b;
	int nbelts;
	struct typeName *typeArray;
};

#endif