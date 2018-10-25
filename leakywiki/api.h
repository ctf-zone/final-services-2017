#ifndef API_H
#define API_H

#include <stdlib.h>

#include "array.h"

#define TOKEN_SIZE 64

int api_initialize(const char *storage_path);

void api_dispose();

int api_generate_token(char *buf, size_t size);

array_t api_get_files(const char *token);

int api_get_file_content(const char *token, const char *filename, char *data, size_t *size);

int api_store_file(const char *token, const char *filename, const char *data, size_t data_len);

#endif