#ifndef NETUTIL_H
#define NETUTIL_H

#include <uv.h>

int create_listener(const char *ip, uint16_t port,
                    uv_loop_t* loop, uv_connection_cb cb,
                    void *cb_data, uv_tcp_t *listener);

#endif