# Define required macros here
SHELL = /bin/sh

TARGET = test
OBJS =  test.cpp functions.cpp functions.h
CFLAG = -Wall -g
CC = g++

.PHONY : run
run : ${TARGET}.o
	./${TARGET}.o ${ARGS} 

${TARGET}.o : ${OBJ}
	${CC} ${CFLAGS} ${OBJS} -o $@

clean:
	-rm -f *.o core *.core
