#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#include "httpserver.h"
#include "log.h"
#include "api.h"
#include "util.h"

#define MAX_WORKER_COUNT 32

static pid_t g_worker_pids[MAX_WORKER_COUNT];
static int g_worker_count;
static int g_should_restart_child = 1;

static void worker()
{
    signal(SIGPIPE, SIG_IGN);
    signal(SIGINT, SIG_DFL);
    signal(SIGTERM, SIG_DFL);
 
    uv_loop_t loop;
    uv_loop_init(&loop);

    if (http_server_init(&loop, "0.0.0.0", 1337) != 0)
    {
        error("Failed to initialized http server");
        goto error_and_dispose;
    }

    info("Start worker");

    uv_run(&loop, UV_RUN_DEFAULT);

    error("Exited from loop");

error_and_dispose:
    api_dispose();
    exit(EXIT_FAILURE);
}

static pid_t start_worker()
{
    pid_t pid = fork();

    if (pid != 0)
        return pid;

    worker();
}

static void restart_worker(pid_t pid)
{
    for (int i = 0; i < g_worker_count; i++)
    {
        if (pid == g_worker_pids[i])
        {
            g_worker_pids[i] = start_worker();
            break;
        }
    }
}

static void sig_handler(int signum)
{
    g_should_restart_child = 0;

    for (int i = 0; i < g_worker_count; i++)
    {
        if (g_worker_pids[i] == 0)
            return;

        info("Send %s to child %d", strsignal(signum), g_worker_pids[i]);

        kill(g_worker_pids[i], signum);
    }
}

int main(int argc, char **argv)
{
    set_log_level(ERROR);

    g_worker_count = MIN(get_cpu_count(), MAX_WORKER_COUNT);

    if (api_initialize("storage") != 0)
    {
        error("Failed to initialized api");
        goto error;
    }

    if (signal(SIGINT, sig_handler) == SIG_ERR)
    {
        error("Failed to set SIGINT handler: %s", strerror(errno));
        goto error_and_dispose;
    }

    if (signal(SIGTERM, sig_handler) == SIG_ERR)
    {
        error("Failed to set SIGTERM handler: %s", strerror(errno));
        goto error_and_dispose;
    }

    for (int i = 0; i < g_worker_count; i++)
    {
        g_worker_pids[i] = start_worker();
    }

    int status = 0;
    do
    {
        pid_t pid = wait(&status);

        if (!g_should_restart_child)
            break;

        if (WIFEXITED(status) || WIFSIGNALED(status))
        {
            restart_worker(pid);
        }
    }
    while (1);
 
error_and_dispose:
    api_dispose();
error:
    return 1;
}