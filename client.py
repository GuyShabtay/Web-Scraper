import socket

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    while True:
        filename = input('Input filename you want to send: ')
        try:
            with open(filename, 'rb') as fi:
                data = fi.read()
                sock.sendall(data)
                print('File sent successfully!')
                break

        except FileNotFoundError:
            print('File not found! Please enter a valid filename.')
