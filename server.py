'''
not <{entirely}> written by me
    ~Wolfy
'''
import socket
import threading
import asyncio
HEADER = 128
PORT = 42069
#SERVER_ADRESS = socket.gethostbyname(socket.gethostname())
SERVER_ADRESS = '127.0.0.1'
FORMAT = 'utf-8'
ADDR = (SERVER_ADRESS, PORT)
DISCONNECT = 'disconnect69'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

class User:
    user_id = None
    conn = None
    addr = None
    thread = None
    connected = False
    def __init__(self,conn,addr,user_id) -> None:
        self.user_id = user_id
        self.conn = conn
        self.addr = addr
        self.thread = threading.Thread(target=self.listen(),args =())
        self.thread.start()


    def listen(self):
        self.connected = True
        while True:
            msg_length = self.conn.recv(HEADER).decode(FORMAT)
            if msg_length != '':
                msg_length = int(msg_length)
                data = self.conn.recv(msg_length).decode(FORMAT)
                if data == DISCONNECT:
                    break
                print(data)
        self.cleanup()

    def cleanup(self):
        self.conn.close()
        self.connected = False
        # self.thread.join() would deadlock!

    def __repr__(self):
        return f'{str(self.user_id)}: {self.addr}'


def start():
    global user_list
    user_list = []
    server_socket.listen()
    server_socket.settimeout(4)
    print(f'[SERVER IS LISTENING TO: {ADDR}]')
    while True:
        try:
            conn, addr = server_socket.accept()
            user_list.append(User(conn,addr,len(user_list)))
        except socket.error:
            pass
        finally:
            for user in user_list:
                if not user.connected:
                    user_list.remove(user)
            print(f'[ACTIVE CONNECTIONS]: {len(user_list)}')

if __name__ == '__main__':
    start()
