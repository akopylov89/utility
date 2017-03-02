#! /usr/bin/python
"""Module with classes for sshpass commands building"""


class SshpassBaseCommandBuilder(object):
    """class to build 'sshpass any_command'"""
    def __init__(self, command):
        self.command = command
        self.executable_command = ['sshpass']
        self.password = None
        self.password_file = None

    def set_password(self, password):
        """method to set password"""
        self.password = password
        return self

    def set_file(self, password_file):
        """method to set password file"""
        self.password_file = password_file
        return self

    def add_executable_command(self):
        return self.command

    def to_build(self):
        """method to build full sshpass command"""
        if self.password and self.password_file:
            raise Exception('Only one of password and password file '
                            'should be set')
        elif self.password:
            password_key = '-p'
            self.executable_command.extend([password_key, self.password])
        elif self.password_file:
            file_key = '-f'
            self.executable_command.extend([file_key, self.password_file])
        else:
            raise Exception('Either password or password file should be set')
        self.executable_command.extend(self.add_executable_command())
        return self.executable_command


class SshCommandBuilder(SshpassBaseCommandBuilder):
    """class to build ssh connection command"""
    def __init__(self, username, cmd):
        super(SshCommandBuilder, self).__init__(command=['ssh'])
        self.username = username
        self.cmd = cmd
        self.ip_address = None
        self.hostname = None

    def set_ip_address(self, ip_address):
        """method to set ip address of a remote host"""
        self.ip_address = ip_address
        return self

    def set_hostname(self, hostname):
        """method to set name of a remote host"""
        self.hostname = hostname
        return self

    def add_executable_command(self):
        """method to build full ssh command with sshpass in the beginning"""
        if self.ip_address and self.hostname:
            raise Exception('Only one of ip address or hostname should be set')
        elif self.ip_address:
            self.command.append('{0}@{1}'.format(self.username,
                                                 self.ip_address))
        elif self.hostname:
            self.command.append('{0}@{1}'.format(self.username,
                                                 self.hostname))
        else:
            raise Exception('Either ip address or hostname should be set')
        self.command.extend(self.cmd)
        return self.command


class IperfKillCommandBuilder(SshCommandBuilder):
    """class to build ssh connection with iperf killing command"""
    def __init__(self, username):
        super(IperfKillCommandBuilder, self)\
            .__init__(username, cmd=['pkill', '-9', 'iperf', ';echo', '$?'])


class ScpConnectionBuilder(SshpassBaseCommandBuilder):
    """class to build scp connection command"""
    def __init__(self, cmd):
        super(ScpConnectionBuilder, self).__init__(command=['scp'])
        self.cmd = cmd
        self.ip_address = None
        self.hostname = None
