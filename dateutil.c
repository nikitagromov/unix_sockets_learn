#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include "unp.h"



int main(int argc, const char * argv[]) {
    int     sockfd;
    ssize_t n;
    char    recvline[MAXLINE + 1];
    struct  sockaddr_in servaddr;
    int i;

    if (argc != 2) {
        printf("WRONG ARGS NUMBER %d\n", argc);
        return 1;
    }

    for (i = 0; i < argc; i++ ) {
        printf( "argv[ %d ] = %s\n", i, argv[ i ] );
    }

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("COULD NOT CREATE SOCKET");
        return 1;
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(13);


    if (inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0) {
        printf("COULD NOT CONVERT ADDRESS TO BINARY");
        err_quit("converting address error");
        return 1;
    }


    if (connect(sockfd, (SA *) &servaddr, sizeof(servaddr)) < 0) {
        printf("COULD NOT CONNECT TO SERVER %s", argv[1]);
        err_sys("connection error");
        return 1;
    }


    while((n = read(sockfd, recvline, MAXLINE)) > 0) {
        recvline[n] = 0;
        if (fputs(recvline, stdout) == EOF) {
            printf("FPUTS ERROR");
            return 1;
        }
    }

    if (n < 0) {
        err_sys("Read error");
    }

    printf("%s", recvline);

    return 0;
}

