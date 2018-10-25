cmake_minimum_required(VERSION 2.8.11)

project(pwn)

add_executable(pwn
	pwn.c
	log.c
	api.c
	httpserver.c
	netutil.c
	util.c
	hashtable.c
	array.c
	httputil.c
	hash.c
	# parson lib
	parson/parson.c
)

include_directories(h2o/include)

add_subdirectory(h2o)

target_link_libraries(pwn
	libh2o
)