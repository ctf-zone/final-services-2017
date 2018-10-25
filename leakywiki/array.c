#include "array.h"

struct array
{
	size_t capacity;
	size_t n;
	void **data;
	void (*release)(void *elem);
};

array_t array_create(size_t capacity, void (*release)(void *elem))
{
	array_t arr = (array_t)malloc(sizeof(struct array));
	if (arr == NULL)
		return NULL;

	arr->capacity = capacity;
	arr->n = 0;
	arr->data = (void **)calloc(capacity, sizeof(void *));
	arr->release = release;

	return arr;
}

static void array_grow(array_t arr, size_t capacity)
{
	arr->capacity = capacity;
	arr->data = (void **)realloc(arr->data, capacity * sizeof(void *));
}

void array_append(array_t arr, void *elem)
{
	arr->data[arr->n++] = elem;

	if (arr->n > arr->capacity)
		array_grow(arr, arr->capacity * 2);
}

void *array_at(array_t arr, size_t idx)
{
	if (idx > arr->n)
		return NULL;

	return arr->data[idx];
}

void **array_data(array_t arr)
{
	return arr->data;
}

size_t array_size(array_t arr)
{
	return arr->n;
}

void array_free(array_t arr)
{
	for (size_t i = 0; i < arr->n; i++)
	{
		if (arr->release)
			arr->release(arr->data[i]);
	}

	free(arr->data);
	free(arr);
}