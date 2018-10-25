#ifndef HTTP_SERVER
#define HTTP_SERVER

#include <stdint.h>
#include <uv.h>

int http_server_init(uv_loop_t *loop, const char *ip, uint16_t port);

#endif