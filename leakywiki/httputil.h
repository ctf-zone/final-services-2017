#ifndef HTTPUTIL_H
#define HTTPUTIL_H

#include <stdlib.h>
#include "hashtable.h"

size_t parse_query(const char *query,
                size_t query_len,
                void (*cb)(void *data, const char *key, const char *value),
                void *data);

hashtable_t get_parameters(const char *query, size_t query_len);

#endif