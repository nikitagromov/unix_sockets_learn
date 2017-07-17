import sys
import json
import os

import docker

workdir = os.path.dirname(os.path.abspath(__file__))
docker_file_path = workdir + '/Dockerfile'
cmd_args = ['./' + sys.argv[1]] + sys.argv[2:]


Dockerfile = '''
FROM gcc:4.9


RUN apt-get update && apt-get install libsctp-dev -y
RUN apt-get install apt-file -y && \
	apt-file update && \
	apt-file search if_dl.h && \
	apt-get install freebsd-glue -y && \
	apt-get install git

RUN mkdir /usr/src/myapp && \
	cd /usr/src/myapp && \
	git clone https://github.com/nikitagromov/Unix-Network-Programming.git && \
	sed -i "60s/size_t size/socklen_t size/" /usr/src/myapp/Unix-Network-Programming/libfree/inet_ntop.c



WORKDIR /usr/src/myapp/Unix-Network-Programming/intro/

RUN cd /usr/src/myapp/Unix-Network-Programming && chmod a+x -R configure && ./configure && \
	cd lib && make && \ 
	cd ../libfree && make

COPY ./{app_name}.c /usr/src/myapp/Unix-Network-Programming/intro/
COPY ./Makefile	/usr/src/myapp/Unix-Network-Programming/intro/

RUN cd /usr/src/myapp/Unix-Network-Programming/intro/ && make {app_name}

CMD {cmd_args}
'''.format(app_name=sys.argv[1], cmd_args=json.dumps(cmd_args))

with open(docker_file_path, 'w') as f:
    f.write(Dockerfile)

print(docker_file_path)
client = docker.from_env()

for line in client.api.build(path=workdir, tag='app:latest', decode=True):
    print(line)
    if 'errorDetail' in  line:
        sys.exit(1)

logs = client.containers.run(image='app:latest',
                      ports={8080: 9999})
print('container started')
print(logs.decode('utf8'))
