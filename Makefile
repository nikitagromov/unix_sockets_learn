include ../Make.defines

PROGS =	myapp

all:	${PROGS}

dateutil:		dateutil.o
	 		${CC} ${CFLAGS} -o $@ dateutil.o ${LIBS}


clean:
		rm -f ${PROGS} ${CLEANFILES}