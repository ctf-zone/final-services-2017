#include <errno.h>
#include <limits.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include "h2o.h"
#include "h2o/http1.h"
#include "h2o/http2.h"
#include "h2o/memcached.h" 

#include "httpserver.h"
#include "netutil.h"
#include "log.h"
#include "api.h"
#include "httputil.h"
#include "hashtable.h"
#include "util.h"
#include "hash.h"

#include "parson/parson.h"

#define USE_MEMCACHED
#define MAX_FILE_SIZE (1024 * 1024)

static char g_filebuf[MAX_FILE_SIZE];

static h2o_pathconf_t *register_handler(h2o_hostconf_t *hostconf,
										const char *path,
										int (*on_req)(h2o_handler_t *, h2o_req_t *))
{
    h2o_pathconf_t *pathconf = h2o_config_register_path(hostconf, path, 0);
    h2o_handler_t *handler = h2o_create_handler(pathconf, sizeof(*handler));
    handler->on_req = on_req;
    return pathconf;
}
 
static void http_on_accept(uv_stream_t *listener, int status)
{
    uv_tcp_t *conn;
    h2o_socket_t *sock;
 
    if (status != 0)
        return;
 
 	h2o_accept_ctx_t *accept_ctx = (h2o_accept_ctx_t *)listener->data;

    conn = h2o_mem_alloc(sizeof(*conn));
    uv_tcp_init(listener->loop, conn);
 
    if (uv_accept(listener, (uv_stream_t *)conn) != 0)
    {
        uv_close((uv_handle_t *)conn, (uv_close_cb)free);
        return;
    }
 
    sock = h2o_uv_socket_create((uv_stream_t*)conn, (uv_close_cb)free);
    h2o_accept(accept_ctx, sock);
}

static int on_error_req(h2o_handler_t *self, h2o_req_t *req, const char *reason)
{
    static h2o_generator_t generator = {NULL, NULL};

    req->res.status = 400;
    req->res.reason = "ERROR";

    char is_persistent = req->http1_is_persistent;

    h2o_add_header(&req->pool, &req->res.headers,
    			   H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/json"));
    h2o_start_response(req, &generator);

    JSON_Value *root_value = json_value_init_object();
    JSON_Object *root_object = json_value_get_object(root_value);

    json_object_set_string(root_object, "status", "ERROR");
    json_object_set_string(root_object, "error", reason);

    char *json = json_serialize_to_string(root_value);

    h2o_iovec_t body = h2o_strdup(&req->pool, json, SIZE_MAX);

    json_free_serialized_string(json);
    json_value_free(root_value);

    // h2o closes connection is response status is error (4xx or 5xx)
    // so setup http1_is_persistent flag here to prevent it
    req->http1_is_persistent = is_persistent;

    h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);

	return 0;
}

static int on_token_req(h2o_handler_t *self, h2o_req_t *req)
{
    static h2o_generator_t generator = {NULL, NULL};

    info("Got generate token request");

	if (!h2o_memis(req->method.base, req->method.len, H2O_STRLIT("GET")))
        return on_error_req(self, req, "Invalid method");

    if (!h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/token/")) &&
        !h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/token")) ||
        req->query_at != SIZE_MAX)
        return on_error_req(self, req, "Invalid request");

    req->res.status = 200;
    req->res.reason = "OK";

    h2o_add_header(&req->pool, &req->res.headers,
    			   H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/json"));
    h2o_start_response(req, &generator);

    char token[TOKEN_SIZE + 1];
    int res = api_generate_token(token, sizeof(token));

    JSON_Value *root_value = json_value_init_object();
    JSON_Object *root_object = json_value_get_object(root_value);

    if (res == 0)
    {
    	json_object_set_string(root_object, "status", "OK");
    	json_object_set_string(root_object, "token", token);
    }
    else
    {
		json_object_set_string(root_object, "status", "ERROR");    	
    }

    char *json = json_serialize_to_string(root_value);

    h2o_iovec_t body = h2o_strdup(&req->pool, json, SIZE_MAX);

    json_free_serialized_string(json);
    json_value_free(root_value);

    h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);

	return 0;
}

static int on_list_req(h2o_handler_t *self, h2o_req_t *req)
{
    static h2o_generator_t generator = {NULL, NULL};

    info("Got list files request");

    if (!h2o_memis(req->method.base, req->method.len, H2O_STRLIT("GET")))
        return on_error_req(self, req, "Invalid method");

    if (!h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/list/")) &&
        !h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/list")))
        return on_error_req(self, req, "Invalid request");

    if (req->query_at == SIZE_MAX)
        return on_error_req(self, req, "Missing parameter");

    size_t query_len = req->path.len - req->query_at;

    hashtable_t ht = get_parameters(req->path.base + req->query_at, query_len);

    const char *token = (const char *)hashtable_get(ht, "token");
    if (token == NULL)
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Missing parameter");
    }

    if (!is_valid_token(token))
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Invalid token");
    }

	req->res.status = 200;
    req->res.reason = "OK";

    h2o_add_header(&req->pool, &req->res.headers,
                   H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/json"));
    h2o_start_response(req, &generator);

    JSON_Value *root_value = json_value_init_object();
    JSON_Object *root_object = json_value_get_object(root_value);

    array_t files = api_get_files(token);

    if (files != NULL)
    {
        json_object_set_string(root_object, "status", "OK");

        JSON_Value *files_value = json_value_init_array();
        JSON_Array *files_array = json_value_get_array(files_value);

        for (size_t i = 0; i < array_size(files); i++)
        {
            const char *filename = (const char *)array_at(files, i);
            json_array_append_string(files_array, filename);
        }

        json_object_set_value(root_object, "files", files_value);

        array_free(files);
    }
    else
    {
        json_object_set_string(root_object, "status", "ERROR");
    }

	char *json = json_serialize_to_string(root_value);
    
    h2o_iovec_t body = h2o_strdup(&req->pool, json, SIZE_MAX);

    json_free_serialized_string(json);
    json_value_free(root_value);

    h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);

    hashtable_free(ht);

    return 0;
}

static int on_upload_req(h2o_handler_t *self, h2o_req_t *req)
{
    static h2o_generator_t generator = {NULL, NULL};

    info("Got upload files request");

    if (!h2o_memis(req->method.base, req->method.len, H2O_STRLIT("POST")))
        return on_error_req(self, req, "Invalid method");

    if (!h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/upload/")) &&
        !h2o_memis(req->path_normalized.base, req->path_normalized.len, H2O_STRLIT("/api/upload")))
        return on_error_req(self, req, "Invalid request");

    for (size_t i = 0; i != req->headers.size; ++i)
    {
        h2o_header_t header = req->headers.entries[i];
        if (h2o_memis(header.name->base, header.name->len, H2O_STRLIT("content-type")))
        {
            if (!h2o_memis(header.value.base, header.value.len, H2O_STRLIT("application/json")))
            {
                return on_error_req(self, req, "Invalid request");
            }
        }
    }

    if (req->query_at == SIZE_MAX)
        return on_error_req(self, req, "Missing parameter");

    size_t query_len = req->path.len - req->query_at;

    hashtable_t ht = get_parameters(req->path.base + req->query_at, query_len);

    const char *error_msg;

    const char *token = (const char *)hashtable_get(ht, "token");
    if (token == NULL)
    {
        error_msg = "Missing parameter";
        goto ret_error;
    }

    if (!is_valid_token(token))
    {
        error_msg = "Invalid token";
        goto ret_error;
    }

    // parse entity
    char *json = (char *)malloc(req->entity.len + 1);
    memcpy(json, req->entity.base, req->entity.len);
    json[req->entity.len] = '\0';

    JSON_Value *json_value = json_parse_string(json);
    if (json_value == NULL)
    {
        error_msg = "Invalid json data";
        goto ret_error;
    }

    JSON_Object *json_object = json_value_get_object(json_value);
    const char *filename = json_object_get_string(json_object, "filename");
    if (filename == NULL || !is_valid_filename(filename))
    {
        error_msg = "Invalid json data";
        goto ret_error;
    }

    const char *b64data = json_object_get_string(json_object, "data");
    if (b64data == NULL)
    {
        error_msg = "Invalid json data";
        goto ret_error;
    }

    size_t decoded_size = 0;
    if ((decoded_size = b64decode(b64data, g_filebuf, NULL)) <= 0)
    {
        error_msg = "Invalid base64 data";
        goto ret_error;
    }

    int res = api_store_file(token, filename, g_filebuf, decoded_size);

    hashtable_free(ht);
    json_value_free(json_value);
    free(json);

    req->res.status = 200;
    req->res.reason = "OK";

    h2o_add_header(&req->pool, &req->res.headers,
                   H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/json"));
    h2o_start_response(req, &generator);

    JSON_Value *root_value = json_value_init_object();
    JSON_Object *root_object = json_value_get_object(root_value);

    if (res == decoded_size)
    {
        json_object_set_string(root_object, "status", "OK");
    }
    else
    {
        json_object_set_string(root_object, "status", "ERROR");
        json_object_set_string(root_object, "error", "Cannot store file");
    }

    json = json_serialize_to_string(root_value);
    
    h2o_iovec_t body = h2o_strdup(&req->pool, json, SIZE_MAX);

    json_free_serialized_string(json);
    json_value_free(root_value);

    h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);

    return 0;

ret_error:
    hashtable_free(ht);
    free(json);
    if (json_value != NULL)
        json_value_free(json_value);

    return on_error_req(self, req, error_msg);
}

static int on_download_req(h2o_handler_t *self, h2o_req_t *req)
{
    static h2o_generator_t generator = {NULL, NULL};

    info("Got download file request");
    
    if (!h2o_memis(req->method.base, req->method.len, H2O_STRLIT("GET")))
        return on_error_req(self, req, "Invalid method");

    char *path = (char *)malloc(req->path_normalized.len + 1);
    memcpy(path, req->path_normalized.base, req->path_normalized.len);
    path[req->path_normalized.len] = '\0';

    char *components[4];

    int res = get_path_components(path, components, sizeof(components) / sizeof(*components));
    if (res != 4)
        return on_error_req(self, req, "Invalid request");

    const char *token = components[2];
    const char *filename = components[3];

    size_t size = 0;
    res = api_get_file_content(token, filename, NULL, &size);
    if (res < 0)
        return -1;

    req->res.status = 200;
    req->res.reason = "OK";

    h2o_start_response(req, &generator);

    char *data = h2o_mem_alloc_pool(&req->pool, size);
    res = api_get_file_content(token, filename, data, &size);
    free(path);

    if (res == size)
    {
        h2o_add_header(&req->pool, &req->res.headers,
                       H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/octet-stream"));

        h2o_iovec_t body = {data, size};
        h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);
    }
    else
    {
        return on_error_req(self, req, "Cannot get file");
    }

    return 0;
}

static int on_get_req(h2o_handler_t *self, h2o_req_t *req)
{
    static h2o_generator_t generator = {NULL, NULL};

    info("Got get file request");

    if (!h2o_memis(req->method.base, req->method.len, H2O_STRLIT("GET")))
        return on_error_req(self, req, "Invalid method");

    if (req->query_at == SIZE_MAX)
        return on_error_req(self, req, "Missing parameter");

    size_t query_len = req->path.len - req->query_at;

    hashtable_t ht = get_parameters(req->path.base + req->query_at, query_len);

    const char *token = (const char *)hashtable_get(ht, "token");
    if (token == NULL)
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Missing parameter");
    }

    if (!is_valid_token(token))
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Invalid token");
    }

    const char *filename = (const char *)hashtable_get(ht, "filename");
    if (filename == NULL)
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Missing parameter");
    }

    if (!is_valid_filename(filename))
    {
        hashtable_free(ht);
        return on_error_req(self, req, "Invalid filename");
    }

    size_t size = 0;
    int res = api_get_file_content(token, filename, NULL, &size);
    if (res < 0)
        return on_error_req(self, req, "Cannot get file");

    req->res.status = 200;
    req->res.reason = "OK";

    h2o_start_response(req, &generator);

    res = api_get_file_content(token, filename, g_filebuf, &size);

    if (res == size)
    {
        char file_hash[1024];
        char file_link[1024];

        if (!hash(g_filebuf, size, file_hash))
            return on_error_req(self, req, "Cannot calculate file hash");

        snprintf(file_link, sizeof(file_link), "/api/download/%s/%s", token, filename);

        h2o_add_header(&req->pool, &req->res.headers,
                       H2O_TOKEN_CONTENT_TYPE, NULL, H2O_STRLIT("application/json"));

        JSON_Value *root_value = json_value_init_object();
        JSON_Object *root_object = json_value_get_object(root_value);

        json_object_set_string(root_object, "link", file_link);
        json_object_set_string(root_object, "hash", file_hash);

        char *json = json_serialize_to_string(root_value);

        h2o_iovec_t body = h2o_strdup(&req->pool, json, SIZE_MAX);

        json_free_serialized_string(json);
        json_value_free(root_value);

        h2o_send(req, &body, 1, H2O_SEND_STATE_FINAL);
    }
    else
    {
        return on_error_req(self, req, "Cannot get file");
    }

    return 0;
}

static int on_api_not_found(h2o_handler_t *self, h2o_req_t *req)
{
    return on_error_req(self, req, "Invalid API method");
}

int http_server_init(uv_loop_t *loop, const char *ip, uint16_t port)
{
	static uv_tcp_t listener;
 	static h2o_globalconf_t config;
 	static h2o_context_t ctx;
 	static h2o_multithread_receiver_t libmemcached_receiver;
 	static h2o_accept_ctx_t accept_ctx;

    h2o_config_init(&config);
    config.max_request_entity_size = MAX_FILE_SIZE;

    h2o_hostconf_t *hostconf = h2o_config_register_host(&config,
    													h2o_iovec_init(H2O_STRLIT("default")),
    													65535);

    register_handler(hostconf, "/api/token", on_token_req);
    register_handler(hostconf, "/api/list", on_list_req);
    register_handler(hostconf, "/api/upload", on_upload_req);
    register_handler(hostconf, "/api/get", on_get_req);
    register_handler(hostconf, "/api/download", on_download_req);
    register_handler(hostconf, "/api", on_api_not_found);

    h2o_pathconf_t *pathconf = h2o_config_register_path(hostconf, "/", 0);
    h2o_file_register(pathconf, "static", NULL, NULL, 0);

    h2o_errordoc_t errordoc = {404, H2O_STRLIT("/404.html")};
    h2o_errordoc_register(pathconf, &errordoc, 1);
 
    h2o_context_init(&ctx, loop, &config);

#ifdef USE_MEMCACHED
    h2o_multithread_register_receiver(ctx.queue, &libmemcached_receiver, h2o_memcached_receiver);
#endif

    accept_ctx.ctx = &ctx;
    accept_ctx.hosts = config.hosts;
 	
    if (create_listener(ip, port, loop, http_on_accept, &accept_ctx, &listener) != 0)
    {
        error("Failed to listen to %s:%d", ip, port);
        return -1;
    }

    return 0;
}