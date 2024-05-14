import socket

def start_server():
    # 創建一個 TCP/IP 伺服器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 綁定伺服器到指定的端口
    server_address = ('localhost', 12345)
    print('Starting server on %s port %s' % server_address)
    server_socket.bind(server_address)

    # 監聽連接
    server_socket.listen(1)

    while True:
        # 等待連接
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        try:
            print('Connection from', client_address)

            while True:
                # 接收字串
                data = connection.recv(1024).decode().strip()
                if not data:
                    break  # 如果沒有接收到資料，則退出循環

                print('Received:', data)

        finally:
            # 關閉連接
            connection.close()

if __name__ == '__main__':
    start_server()
