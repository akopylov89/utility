#! /usr/bin/python
"""Module with 'iperf' commands construction for server and client"""


class BaseIperfCommandBuilder(object):
    """base command builder for iperf server and client"""
    def __init__(self, mode=None):
        self.command = ['iperf']
        self.mode = mode
        self.mode_udp = None
        self.port = None
        self.check_of_execution = None

    def set_mode_udp(self, udp):
        """method to set server using UDP"""
        self.mode_udp = udp
        return self

    def set_port(self, port):
        """method to set server port to listen"""
        self.port = port
        return self

    def set_checking_of_execution(self):
        """method to set checking of command exit code"""
        self.check_of_execution = [';echo', '$?']
        return self


class IperfServerCommandBuilder(BaseIperfCommandBuilder):
    """command builder for iperf server"""
    def __init__(self):
        super(IperfServerCommandBuilder, self).__init__(mode='-s')
        self.daemon = None

    def set_as_daemon(self):
        """method to run server as a daemon"""
        self.daemon = '-D'
        return self

    def build_server_command(self):
        """if daemon, port and mode are set - add to server command"""
        self.command.append(self.mode)
        if self.daemon:
            self.command.append(self.daemon)
        if self.mode_udp:
            key_udp = '-u'
            self.command.append(key_udp)
        if self.port:
            key_port = '-p'
            self.command.extend([key_port, self.port])
        if self.check_of_execution:
            self.command.extend(self.check_of_execution)
        return self.command


class IperfClientCommandBuilder(BaseIperfCommandBuilder):
    """command builder for iperf client"""
    def __init__(self):
        super(IperfClientCommandBuilder, self).__init__(mode='-c')
        self.server_ip = None
        self.server_hostname = None
        self.testing_time = None
        self.interval = None

    def set_server_ip(self, server_ip):
        """method to set server ip address"""
        self.server_ip = server_ip
        return self

    def set_server_hostname(self, hostname):
        """method to set server hostname"""
        self.server_hostname = hostname
        return self

    def set_testing_time(self, time):
        """method to set testing time"""
        self.testing_time = time
        return self

    def set_time_interval(self, interval):
        """method to set interval of measurements"""
        self.interval = interval
        return self

    def build_client_command(self):
        """if mode, port, time and interval are set - add to client command"""
        self.command.append(self.mode)
        if self.server_ip and self.server_hostname:
            raise Exception('Only one of server ip and hostname should be set')
        elif self.server_hostname:
            self.command.append(self.server_hostname)
        elif self.server_ip:
            self.command.append(self.server_ip)
        else:
            raise Exception('Either server ip and hostname should be set')
        if self.mode_udp:
            key_udp = '-u'
            self.command.append(key_udp)
        if self.port:
            key_port = '-p'
            self.command.extend([key_port, self.port])
        if self.testing_time:
            key_testing_time = '-t'
            self.command.extend([key_testing_time, self.testing_time])
        if self.interval:
            key_interval = '-i'
            self.command.extend([key_interval, self.interval])
        if self.check_of_execution:
            self.command.extend(self.check_of_execution)
        return self.command
