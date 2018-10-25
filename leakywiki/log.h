#ifndef LOG_H
#define LOG_H

enum log_level
{
	FATAL = 0,
	ERROR,
	INFO
};

void set_log_level(enum log_level level);

void info(const char *fmt, ...);
 
void error(const char *fmt, ...);
 
void fatal(const char *fmt, ...);

#endif