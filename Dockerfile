
FROM gcc:4.9


RUN apt-get update && apt-get install libsctp-dev -y
RUN apt-get install apt-file -y && 	apt-file update && 	apt-file search if_dl.h && 	apt-get install freebsd-glue -y && 	apt-get install git

RUN mkdir /usr/src/myapp && 	cd /usr/src/myapp && 	git clone https://github.com/nikitagromov/Unix-Network-Programming.git && 	sed -i "60s/size_t size/socklen_t size/" /usr/src/myapp/Unix-Network-Programming/libfree/inet_ntop.c



WORKDIR /usr/src/myapp/Unix-Network-Programming/intro/

RUN cd /usr/src/myapp/Unix-Network-Programming && chmod a+x -R configure && ./configure && 	cd lib && make && \ 
	cd ../libfree && make

COPY ./dateutil.c /usr/src/myapp/Unix-Network-Programming/intro/
COPY ./Makefile	/usr/src/myapp/Unix-Network-Programming/intro/

RUN cd /usr/src/myapp/Unix-Network-Programming/intro/ && make dateutil

CMD ["./dateutil", "129.6.15.28"]
