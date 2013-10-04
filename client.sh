#!/bin/bash

PORT=8080
HOST='localhost'

test_single(){
    printf "GET / HTTP:1/1\r\nHost: localhost\r\n\r\n" | nc $HOST $PORT
}

test_multi(){
    printf "GET / HTTP:1/1\r\nHost: localhost\r\n\r\nGET /index.html HTTP:1/1\r\nHost: localhost\r\n\r\n" #| nc $HOST $PORT
}

test_long() {
    printf "GET / HTTP:1/1\r\nHost: localhost\r\nAccept-Language: en-US\r\nAccept-Encoding: gzip,deflate,sdch\r\nConnection: keep-alive\r\nAccept: text/html\r\nUser-Agent: BashScript\r\n\r\n" | nc $HOST $PORT
}

#~ test_long
#~ test_single
test_multi
