from socket import *

host = '192.168.1.127'
port = 8888
addr = (host, port)

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind(addr)
tcp_socket.listen(1)

while True:
    print('wait connection...')

    conn, addr = tcp_socket.accept()
    print('client addr: ', addr)
    data = conn.recv(1024)

    if not data:
        #conn.send(b'ERROR!\n')
        conn.close()

    elif data == b'date\n':
        conn.send(b'DATE!\n')
        conn.close()

    elif data == b'help\n':
        conn.send(b'''Available commands:
            date: Return current date and time
            myip: Return client's IP address
            help: See this help message\n''')
        conn.close()

    elif data == b'myip\n':
        conn.send(str.encode(addr[0]) + b'\n')
        conn.close()
    else:
        print(data)
        enc = data.decode('utf-8')
        enc = enc.rstrip('\n')
        conn.send(b'ERROR! The command ' + str.encode(enc) + b' is unknown! Use "help" to see all available commands.\n')
        conn.close()

tcp_socket.close()

