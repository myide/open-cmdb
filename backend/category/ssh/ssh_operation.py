import json
import os

from django.conf import settings
from rest_framework.exceptions import ParseError

from category.models import Server

from .ssh_connection import SSHConnection


class SSHOperation(object):

    def __init__(self, host, port, user):
        self.host = host
        self.port = port
        self.user = user
        self.cron_dir = '/var/spool/cron/'

    @staticmethod
    def __operate(action):
        try:
            return action
        except Exception as e:
            raise ParseError(e)

    def __conn(self):
        ssh_conn = SSHConnection(host=self.host, port=self.port, user=self.user, key_file=settings.KEY_FILE)
        return self.__operate(ssh_conn)

    def __upload(self, path_local, path_remote):
        conn = self.__conn()
        return self.__operate(conn.upload(path_local, path_remote))

    def __download(self, path_local, path_remote):
        conn = self.__conn()
        return self.__operate(conn.download(path_local, path_remote))

    def __cmd(self, command):
        conn = self.__conn()
        return self.__operate(conn.cmd(command))

    def fetch_host_info(self, source_data, ssh_user):
        path_local = 'scripts/sys_info'
        path_remote = '/tmp/sys_info'
        self.__upload(path_local, path_remote)
        command = "chmod +x {} && sudo {} {}".format(path_remote, path_remote, ssh_user)
        data = self.__cmd(command)
        if not data:
            raise ParseError('未获取到客户机数据')
        data = json.loads(data)
        source_data['uuid'] = data['uuid']
        source_data['system_product'] = data['system_product']
        source_data['disk'] = data['disk']
        source_data['cpu'] = data['cpu']['version']
        source_data['memory'] = data['memory']
        source_data['name'] = data['name']
        return source_data

    def fetch_cron_content(self, filename):
        file_path = '{}{}'.format(self.cron_dir, filename)
        command = "sudo cat {}".format(file_path)
        data = self.__cmd(command)
        return data

    def fetch_cron_log(self, user, count=100):
        command = "sudo tail -{} /var/log/cron|grep CROND|grep {}".format(count, user)
        data = self.__cmd(command)
        return data

    def update_cron_file(self, filename, content):
        tmp_file = '/tmp/{}'.format(filename)
        remote_path = '{}{}'.format(self.cron_dir, filename)
        with open(tmp_file, 'w') as f:
            f.write(content)
        self.__upload(tmp_file, tmp_file)
        command = "sudo mv {} {} && sudo chmod 644 {}".format(tmp_file, remote_path, remote_path)
        self.__cmd(command)
        os.remove(tmp_file)

    def sync_cron_file(self, filename, servers):
        content = self.fetch_cron_content(filename)
        servers = servers.get('servers')
        ips = []
        for pk in servers:
            instance = Server.objects.get(pk=pk)
            username = instance.ssh_user.name
            ssh_operation = SSHOperation(instance.ssh_ip, instance.ssh_port, username)
            ssh_operation.update_cron_file(username, content)
            ips.append(instance.ssh_ip)
        return ips
