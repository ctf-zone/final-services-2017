#include "netutil.h"
#include "log.h"

int create_listener(const char *ip, uint16_t port,
                    uv_loop_t* loop, uv_connection_cb cb,
                    void *cb_data, uv_tcp_t *listener)
{
    struct sockaddr_in addr;
    int r;
 
    listener->data = cb_data;

    uv_tcp_init_ex(loop, listener, AF_INET);

    int fd;
    int enable = 1;
    uv_fileno((uv_handle_t *)listener, &fd);
    setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &enable, sizeof(enable));

    uv_ip4_addr(ip, port, &addr);
    
    if ((r = uv_tcp_bind(listener, (struct sockaddr *)&addr, 0)) != 0)
    {
        error("uv_tcp_bind: %s", uv_strerror(r));
        goto error;
    }
    
    if ((r = uv_listen((uv_stream_t *)listener, 128, cb)) != 0)
    {
        error("uv_listen: %s", uv_strerror(r));
        goto error;
    }
 
    return 0;

error:
    uv_close((uv_handle_t *)listener, NULL);
    return -1;
}