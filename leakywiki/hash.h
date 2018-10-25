#ifndef HASH_H
#define HASH_H

#include <stdlib.h>

typedef struct context * context_t;

int hash_init(context_t ctx);

int hash_update(context_t ctx, const char *data, size_t len);

int hash_final(context_t ctx, char *out);

int hash(const char *data, size_t len, char *out);

#endif // HASH_H