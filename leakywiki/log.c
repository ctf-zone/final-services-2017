#include "log.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <sys/types.h>
#include <unistd.h>

#define LOG_BUFSIZE 1024

static enum log_level g_log_level = ERROR;

static const char *log_level_to_string(enum log_level level)
{
    switch (level)
    {
        case INFO:
            return "INFO";
        case ERROR:
            return "ERROR";
        case FATAL:
            return "FATAL";
    }
}

static int should_log(enum log_level level)
{
    if (level > g_log_level)
        return 0;

    return 1;
}

void set_log_level(enum log_level level)
{
    g_log_level = level;
}

void flog(FILE *stream, enum log_level level, const char *fmt, va_list arglist)
{
    char buf[LOG_BUFSIZE];

    if (!should_log(level))
        return;
 
    vsnprintf(buf, sizeof(buf), fmt, arglist);
 
    fprintf(stdout, "[pid %d] [%s] %s\n", getpid(), log_level_to_string(level), buf);
}
 
void info(const char *fmt, ...)
{
    va_list arglist;
    va_start(arglist, fmt);
 
    flog(stdout, INFO, fmt, arglist);
 
    va_end(arglist);
}
 
 
void error(const char *fmt, ...)
{
    va_list arglist;
    va_start(arglist, fmt);
 
    flog(stderr, ERROR, fmt, arglist);
 
    va_end(arglist);
}
 
void fatal(const char *fmt, ...)
{
    va_list arglist;
    va_start(arglist, fmt);
 
    flog(stderr, FATAL, fmt, arglist);
 
    va_end(arglist);
 
    abort();
}