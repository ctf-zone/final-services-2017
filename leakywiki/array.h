#ifndef ARRAY_H
#define ARRAY_H

#include <stdlib.h>

#define DEFAULT_CAPACITY 16

typedef struct array * array_t;

array_t array_create(size_t capacity,
				   void (*release)(void *elem));

void array_append(array_t arr, void *elem);

void *array_at(array_t arr, size_t idx);

void **array_data(array_t arr);

size_t array_size(array_t arr);

void array_free(array_t arr);

#endif