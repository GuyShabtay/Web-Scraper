import socket

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    totalclient = int(input('Enter number of clients: '))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(totalclient)

    connections = []
    print('Initiating clients')
    for i in range(totalclient):
        conn, addr = sock.accept()  # accept returns a tuple (conn, addr)
        connections.append(conn)
        print('Connected with client', i + 1)

    fileno = 0
    idx = 0
    for conn in connections:
        idx += 1
        filename = f'output{fileno}.csv'
        fileno += 1
        with open(filename, 'wb') as fo:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                fo.write(data)

        print()
        print('Receiving file from client', idx)
        print('Received successfully! New filename is:', filename)

    # Closing all Connections
    for conn in connections:
        conn.close()
