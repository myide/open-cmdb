from channels.generic.websocket import WebsocketConsumer
from django.http.request import QueryDict
from .ssh import SSH
from .models import *

class WebSSH(WebsocketConsumer):
    message = {'status': 0, 'message': None}

    def connect(self):
        """
        打开 websocket 连接, 通过前端传入的参数尝试连接 ssh 主机
        :return:
        """
        self.accept()
        query_string = self.scope.get('query_string')
        ssh_args = QueryDict(query_string=query_string, encoding='utf-8')
        server_id = ssh_args.get('server_id')
        user_id = ssh_args.get('user_id')
        server = Server.objects.get(id=server_id)
        user = SSHUser.objects.get(id=user_id)
        self.ssh = SSH(websocker=self, message=self.message)
        ssh_connect_dict = {
            'host': server.ssh_ip,
            'port': server.ssh_port,
            'user': user.name,
            'password': user.password,
            'timeout': 30,
            'pty_width': 500,
            'pty_height': 200,
        }
        self.ssh.connect(**ssh_connect_dict)

    def disconnect(self, close_code):
        self.ssh.close()

    def receive(self, text_data=None, bytes_data=None):
        data = text_data
        self.ssh.shell(data)
