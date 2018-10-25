#include <ctype.h>
#include <string.h>

#include "httputil.h"

size_t parse_query(const char *query,
                size_t query_len,
                void (*cb)(void *data, const char *key, const char *value),
                void *data)
{
    char key[512];
    char value[512];
    char buf[3];

    int j = 0;
    int k = 0;

    char *cur_buf = key;
    size_t cur_size = sizeof(key) - 1;
    size_t count = 0;

    int parse_value = 0;
    int url_decode = 0;

    for (size_t i = 1; i < query_len; i++)
    {
        if (query[i] == '&')
        {
            cur_buf[j] = '\0';
            if (cb && parse_value)
                cb(data, key, value);

            ++count;

            cur_buf = key;
            j = 0;
            parse_value = 0;
        }
        else if (query[i] == '=' && !parse_value)
        {
            cur_buf[j] = '\0';
            cur_buf = value;
            j = 0;
            parse_value = 1;
        }
        else if (query[i] == '%' && !url_decode)
        {
            url_decode = 1;
            k = 0;
        }
        else if (url_decode)
        {
            buf[k++] = query[i];

            if (k == 2)
            {
                buf[k] = '\0';
                url_decode = 0;

                // BOF here
                if (isxdigit(buf[0]) && isxdigit(buf[1]))
                {
                    cur_buf[j++] = (char) strtol(buf, NULL, 16);
                }
                else
                {
                    cur_buf[j++] = '%';
                    cur_buf[j++] = buf[0];
                    cur_buf[j++] = buf[1];
                }
            }
        }
        else
        {
            if (j < cur_size)
                cur_buf[j++] = query[i];
        }
    }

    if (parse_value)
    {
        if (cb)
        {
            if (url_decode && k == 2)
            {
                buf[k] = '\0';
                // BOF here
                if (isxdigit(buf[0]) && isxdigit(buf[1]))
                {
                    cur_buf[j++] = (char) strtol(buf, NULL, 16);
                }
                else
                {
                    cur_buf[j++] = '%';
                    cur_buf[j++] = buf[0];
                    cur_buf[j++] = buf[1];
                }
            }

            cur_buf[j] = '\0';
            cb(data, key, value);
        }

        ++count;
    }

    return count;
}

static void hashtable_release(void *key, void *data)
{
    free(key);
    free(data);
}

static void parse_query_cb(void *data, const char *key, const char *value)
{
    hashtable_t ht = (hashtable_t) data;
    hashtable_insert(ht, strdup(key), strdup(value));
}

hashtable_t get_parameters(const char *query, size_t query_len)
{
    int count = parse_query(query, query_len, NULL, NULL);
    hashtable_t ht = hashtable_create(count, string_hash, string_equals, hashtable_release);
    parse_query(query, query_len, parse_query_cb, ht);
    return ht;
}