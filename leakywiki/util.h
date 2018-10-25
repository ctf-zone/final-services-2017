#ifndef UTIL_H
#define UTIL_H

#include <stdlib.h>
#include <dirent.h>

#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))

int random_bytes(char *buf, size_t size, int use_true_random);

int exists(const char *path, int is_dir);

int list_dir(const char *path,
    int type,
    void (*cb)(void *data, char *filename),
    void *data);

int get_path_components(char *str, char **comp, size_t comp_len);

int is_valid_filename(const char *filename);

int is_valid_token(const char *token);

int b64decode(const char *b64data, char *data, size_t *len);

int get_cpu_count();

#endif