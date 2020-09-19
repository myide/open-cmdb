import json
import socket
from threading import Thread

import paramiko


class SSH:

    def __init__(self, websocket, message):
        self.websocket = websocket
        self.message = message
        self.channel = None

    def connect(self, host, user, password=None, port=22, timeout=30, term='xterm', pty_width=80, pty_height=24,
                private_key=''):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if private_key:
                pkey = paramiko.RSAKey.from_private_key_file(private_key)
                ssh_client.connect(hostname=host, port=port, username=user, pkey=pkey)
            else:
                ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)
            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()
            for i in range(2):
                recv = self.channel.recv(1024).decode('utf-8')
                self.websocket.send(recv)
        except socket.timeout:
            message = 'ssh 连接超时'
            self.websocket.send(message)
            self.close()
        except Exception as e:
            print(e)
            self.close()

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
        except Exception as e:
            print(e)
            self.close()

    def websocket_to_django(self, data):
        self.channel.send(data)
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                if not len(data):
                    return
                self.websocket.send(data)
        except Exception as e:
            print(e)
            self.close()

    def close(self):
        self.message['status'] = 1
        self.message['message'] = 'Close Connection'
        message = json.dumps(self.message)
        self.websocket.send(message)
        self.websocket.close()

    def shell(self, data):
        Thread(target=self.websocket_to_django, args=(data,)).start()
