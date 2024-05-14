import socket

def send_data():
    # 創建一個 TCP/IP 連接
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 連接服務器
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    try:
        while True:
            # 提示用戶輸入文字
            message = input('Enter your message (type "exit" to quit): ')
            if message.lower() == 'exit':
                break

            # 傳送字串
            client_socket.sendall(message.encode())

    finally:
        # 關閉連接
        client_socket.close()

if __name__ == '__main__':
    send_data()
