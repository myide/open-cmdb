import paramiko
import socket
import json
from threading import Thread


class SSH:
    def __init__(self, websocker, message):
        self.websocker = websocker
        self.message = message

    def connect(self, host, user, password=None, port=22, timeout=30,
        term='xterm', pty_width=80, pty_height=24):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(username=user, password=password, hostname=host, port=port, timeout=timeout)
            transport = ssh_client.get_transport()
            self.channel = transport.open_session()
            self.channel.get_pty(term=term, width=pty_width, height=pty_height)
            self.channel.invoke_shell()

            for i in range(2):
                recv = self.channel.recv(1024).decode('utf-8')
                self.websocker.send(recv)
        except socket.timeout:
            message= 'ssh 连接超时'
            self.websocker.send(message)
            self.close()
        except:
            self.close()

    def resize_pty(self, cols, rows):
        self.channel.resize_pty(width=cols, height=rows)

    def django_to_ssh(self, data):
        try:
            self.channel.send(data)
        except:
            self.close()

    def websocket_to_django(self, data):
        self.channel.send(data)
        try:
            while True:
                data = self.channel.recv(1024).decode('utf-8')
                if not len(data):
                    return
                self.websocker.send(data)
        except:
            self.close()

    def close(self):
        self.message['status'] = 1
        self.message['message'] = 'Close Connection'
        message = json.dumps(self.message)
        self.websocker.send(message)
        #self.channel.close()
        self.websocker.close()

    def shell(self, data):
        Thread(target=self.websocket_to_django, args=(data,)).start()
