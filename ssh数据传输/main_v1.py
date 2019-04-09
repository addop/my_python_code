import paramiko


class data_transfer:
    def __init__(self, hostname, username, password):
        self.ssh = paramiko.SSHClient()
        self.hostname = hostname
        self.username = username
        self.password = password

        self.cmd = None
        self.logging = None

    def ssh_communication(self, cmd):
        self.cmd = cmd
        # 创建SSH对象
        # 把要连接的机器添加到known_hosts文件中
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        self.ssh.connect(hostname=self.hostname, port=22,
                         username=self.username, password=self.password)

        stdin, stdout, stderr = self.ssh.exec_command(self.cmd)
        result = stdout.read()
        if not result:
            result = stderr.read()
        self.ssh.close()
        self.logging = result.decode()
        print(self.logging)

    def sftp_transfer(self, landing_path):
        transport = paramiko.Transport(self.hostname, 22)
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        send_data = input('send_data:')
        get_data = input('get_data:')
        if send_data:
            if send_data.split('.')[-1]:
                sftp.put(send_data, landing_path+send_data.split('/')[-1])
            else: # 文件夹
                sftp.put(send_data, landing_path)
        # if get_data:
        #     sftp.get(get_data, landing_path)
        transport.close()
        pass


ccc = data_transfer('192.168.1.118', 'pi', 'Zh19930924')

# ccc.sftp_transfer('Downloads/') # 这里前面不用加~

ccc.ssh_communication('cd /etc/init.d; '
                      'sudo chmod 777 Auto_Start_Test; '
                      'sudo update-rc.d Auto_Start_Test defaults; '
                      'sudo service Auto_Start_Test start; '
                      'sudo reboot')
