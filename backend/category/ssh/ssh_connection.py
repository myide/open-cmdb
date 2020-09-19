import paramiko
from rest_framework.exceptions import ParseError


'''
https://blog.csdn.net/qq_24674131/article/details/95618304

免密登陆的用户
1. 本机到远程做免密
2. 远程用户加入sudoers，并设置免密sudo
'''


class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='xxx.xxx.xxx.xxx', port=22, user='xxx', pwd='xxxxx', key_file=''):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.key_file = key_file
        transport = paramiko.Transport((self.host, self.port))
        if self.key_file:
            try:
                private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
                transport.connect(username=self.user, pkey=private_key)
            except Exception as e:
                raise ParseError(f'用户{self.key_file}免密连接{self.user}@{self.host}:{self.port}失败，')
        else:
            transport.connect(username=self.user, password=self.pwd)
        self.__transport = transport
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path, mode='0777'):
        self.sftp.mkdir(target_path, mode)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def listdir_attr(self, target_path):
        try:
            files = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)
        return files

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        return result.decode('utf8')
