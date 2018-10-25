#include <uv.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

#include <openssl/bio.h>
#include <openssl/evp.h>

#include "util.h"
#include "log.h"

int random_bytes(char *buf, size_t size, int use_true_random)
{
	// Use /dev/random istead of /dev/urandom because in this case
	// we can get incomplete buffer
	int fd;
	if (use_true_random)
	{
		fd = open("/dev/random", O_RDONLY | O_NONBLOCK);
		if (fd < 0)
		{
			error("Cannot open /dev/random");
			return -1;
		}
	}
	else
	{
		fd = open("/dev/urandom", O_RDONLY);
		if (fd < 0)
		{
			error("Cannot open /dev/urandom");
			return -1;
		}
	}

	int nbytes = read(fd, buf, size);

	close(fd);

	return nbytes;
}

int exists(const char *path, int is_dir)
{
	struct stat st;	
	if (stat(path, &st) == 0)
	{
		if (is_dir && S_ISDIR(st.st_mode) || !is_dir && !S_ISDIR(st.st_mode))
			return -1;
	}

	return 0;
}

int list_dir(const char *path,
			 int type,
			 void (*cb)(void *data, char *filename),
			 void *data)
{
	DIR *dir;
	struct dirent *ent;
	int count = 0;
	if ((dir = opendir(path)) != NULL)
	{
		while ((ent = readdir(dir)) != NULL)
		{
			if (strcmp(ent->d_name, ".") == 0 ||
				strcmp(ent->d_name, "..") == 0)
				continue;

			if (type & ent->d_type)
			{
				if (cb != NULL)
					cb(data, ent->d_name);

				++count;
			}
		}
		
		closedir(dir);

		return count;
	}

	return -1;
}

int get_path_components(char *str, char **comp, size_t comp_len)
{
	int i = 0;
	char *token = strtok(str, "/");
	
	while (token != NULL)
	{
		if (comp && i < comp_len)
			comp[i] = token;

		token = strtok(NULL, "/");
	
		++i;
	}

	return i;
}

int is_valid_filename(const char *filename)
{
	return strstr(filename, "/") == NULL;
}

static size_t b64decode_length(const char* b64data)
{
	size_t len = strlen(b64data);
	size_t padding = 0;

	if (b64data[len-1] == '=' && b64data[len-2] == '=')
		padding = 2;
	else if (b64data[len-1] == '=')
		padding = 1;

	return (len * 3) / 4 - padding;
}

int b64decode(const char *b64data, char *data, size_t *len)
{
	if (data == NULL)
	{
		*len = b64decode_length(b64data);
		return 0;
	}

	BIO *bio, *b64;
	bio = BIO_new_mem_buf(b64data, -1);
	b64 = BIO_new(BIO_f_base64());
	bio = BIO_push(b64, bio);

	BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
	size_t length = BIO_read(bio, data, strlen(b64data));
	BIO_free_all(bio);

	return length;
}


int is_valid_token(const char *token)
{
	if (strchr(token, '/'))
		return 0;

	if (strchr(token, '.'))
		return 0;

	return 1;
}

int get_cpu_count()
{
	uv_cpu_info_t *info;
	int cpu_count;

	if (uv_cpu_info(&info, &cpu_count))
		return 1;

	uv_free_cpu_info(info, cpu_count);

	return cpu_count;
}