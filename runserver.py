#!/usr/bin/python3

from socket import *
import os
import logging
import datetime

host = os.popen('ip addr show enp0s3 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
port = 8888
addr = (host, port)

now = datetime.datetime.now()

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind(addr)
tcp_socket.listen(1)


logging.basicConfig(filename='/var/log/py-server.log',level=logging.DEBUG)
logging.info('Starting server')

def CloseCon():
    conn.close()
    logging.info('Closing connetion from ' + str(addr[0]))
def LogExecute(command):
    logging.debug('Trying to execute command ' + str(command))

while True:
    print('wait connection...')

    conn, addr = tcp_socket.accept()
    print('client addr: ', addr)
    logging.info('New connetion from ' + str(addr[0]))
    data = conn.recv(1024)

    if not data:
        CloseCon()

    elif data == b'date\n':
        LogExecute('date')
        conn.send(str.encode(now.strftime("%Y-%m-%d %H:%M")) + b'\n')
        CloseCon()

    elif data == b'help\n':
        LogExecute('help')
        conn.send(b'''Available commands:
            date: Return current date and time
            myip: Return client's IP address
            help: See this help message\n''')
        CloseCon()

    elif data == b'myip\n':
        LogExecute('myip')
        conn.send(str.encode(addr[0]) + b'\n')
        CloseCon()
    else:
        print(data)
        enc = data.decode('utf-8')
        enc = enc.rstrip('\n')
        LogExecute(enc)
        conn.send(b'ERROR! The command ' + str.encode(enc) + b' is unknown! Use "help" to see all available commands.\n')
        CloseCon()

tcp_socket.close()
