#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "api.h"
#include "util.h"
#include "log.h"
#include "hashtable.h"
#include "array.h"

static const char *g_storage_path;

int api_initialize(const char *storage_path)
{
	int res = mkdir(storage_path, ACCESSPERMS);
	if (res != 0 && (errno != EEXIST || !exists(storage_path, 1)))
	{
		error("Cannot create dir '%s': %s", storage_path, strerror(errno));
		return -1;
	}

	g_storage_path = strdup(storage_path);

	return 0;
}

void api_dispose()
{
	free((void *)g_storage_path);
}

static int api_generate_token_internal(char *buf, size_t size)
{
	size_t byte_size = size / 2;
	if ((size & 1) == 0)
		byte_size -= 1;

	char rnd[byte_size];
	size_t off = byte_size / 2;

	random_bytes(rnd, byte_size, 1);
	random_bytes(rnd, off, 0);

	for (size_t i = 0; i < off; i++)
		rnd[i + off] ^= rnd[i];

	for (size_t i = 0; i < byte_size; i++)
		sprintf(&buf[2 * i], "%02hhx", rnd[i]);
	
	return 0;
}

int api_generate_token(char *buf, size_t size)
{
	int res;
	// Special constant to easily leak stack canary
	char path[128];
	while ((res = api_generate_token_internal(buf, size)) == 0)
	{
		snprintf(path, sizeof(path), "%s/%s", g_storage_path, buf);
		res = mkdir(path, ACCESSPERMS);
		if (res == EEXIST)
			continue;

		if (res != 0)
		{
			error("Cannot create dir '%s': %s", path, strerror(errno));
			return -1;
		}

		return 0;
	}

	return res;
}

static void on_list_dir(void *data, char *path)
{
	array_t arr = (array_t) data;
	array_append(arr, strdup(path));
}

array_t api_get_files(const char *token)
{
	char path[1024];
	snprintf(path, sizeof(path), "%s/%s", g_storage_path, token);

	array_t files = array_create(DEFAULT_CAPACITY, free);

	if (list_dir(path, DT_REG, on_list_dir, files) < 0)
	{
		array_free(files);
		return NULL;
	}

	return files;
}

int api_get_file_content(const char *token, const char *filename, char *data, size_t *size)
{
	char path[1024];

	snprintf(path, sizeof(path), "%s/%s/%s", g_storage_path, token, filename);
	
	struct stat st;	
	if (stat(path, &st) == 0)
	{
		if (!S_ISREG(st.st_mode))
			return -1;

		if (data == NULL)
			*size = st.st_size;

		if (data != NULL)
		{
			int fd = open(path, O_RDONLY);
			if (fd > 0)
			{
				int res = read(fd, data, *size);
				close(fd);
				return res;
			}

			error("Cannot open file '%s' for reading: %s", path, strerror(errno));
		}

		return 0;
	}

	return -1;
}

int api_store_file(const char *token, const char *filename, const char *data, size_t data_len)
{
	char path[1024];

	snprintf(path, sizeof(path), "%s/%s/%s", g_storage_path, token, filename);

	int fd = open(path, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
	if (fd < 0)
	{
		error("Cannot open file '%s' for writing: %s", path, strerror(errno));
		return -1;
	}

	int res = write(fd, data, data_len);
	close(fd);

	return res;
}