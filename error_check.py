#! /usr/bin/python
"""Module with classes for error catching"""

remote_host_execution_error = 101
ssh_connection_error = 255
server_firewall_error = 102
server_establishing_error = 103


class MyError(Exception):
    """class of error with message and exit code"""
    def __init__(self, message, return_code):
        self.message = message
        self.return_code = return_code


class BaseErrorExitCodeController(object):
    """class to check if there are errors after subprocess execution
    of a command"""
    def __init__(self, subprocess_exit_code, subprocess_error):
        self.subprocess_exit_code = subprocess_exit_code
        self.subprocess_error = subprocess_error

    def check_if_error(self):
        """method to check if exit code is not 0"""
        if self.subprocess_exit_code:
            raise MyError('Error occurred, {0}'.format(self.subprocess_error),
                          self.subprocess_exit_code)


class SshpassErrorExitCodeController(BaseErrorExitCodeController):
    """class to check if sshpass errors occurred"""
    def __init__(self, subprocess_exit_code, subprocess_error):
        super(SshpassErrorExitCodeController, self)\
            .__init__(subprocess_exit_code, subprocess_error)

    def check_if_error(self):
        """method to check if exit code is in range 1-6"""
        if self.subprocess_exit_code in range(1, 7):
            raise MyError('Sshpass error: exit code {0}, {1}'
                          .format(self.subprocess_exit_code,
                                  self.subprocess_error),
                          self.subprocess_exit_code)


class SshErrorExitCodeController(BaseErrorExitCodeController):
    """class to check if ssh errors occurred"""
    def __init__(self, subprocess_exit_code, subprocess_error):
        super(SshErrorExitCodeController, self)\
            .__init__(subprocess_exit_code, subprocess_error)

    def check_if_error(self):
        """method to check if exit code is 255 - it is ssh error"""
        if self.subprocess_exit_code == 255:
            raise MyError('Ssh error: exit code {0}, {1}'
                          .format(self.subprocess_exit_code,
                                  self.subprocess_error),
                          ssh_connection_error)


class ExecutionExitCodeController(object):
    """class to check if remote executable commands errors occurred"""
    def __init__(self, execution_exit_code, subprocess_error):
        self.subprocess_error = subprocess_error
        self.execution_exit_code = execution_exit_code

    def check_if_error(self):
        """method to check if exit code of remote command is not 0 - it's
        an error, and when exit code is 0 but error message exists - it's
        an error"""
        if self.execution_exit_code:
            raise MyError('Command execution error on a remote host: "{0}"'
                          .format(self.subprocess_error),
                          remote_host_execution_error)
        if not self.execution_exit_code and self.subprocess_error:
            raise MyError('Command execution error on a remote host: "{0}"'
                          .format(self.subprocess_error),
                          remote_host_execution_error)


class OtherErrorsChecking(BaseErrorExitCodeController):
    """class to check if remote host is working correctly"""
    def check_if_error(self):
        """method to check if there is a server firewall error and if
        remote host is working"""
        if self.subprocess_error == "connect failed: No route to host\n":
            raise MyError('Server firewall error', server_firewall_error)
        if self.subprocess_error == "connect failed: Connection refused\n":
            raise MyError('Iperf server establishing error',
                          server_establishing_error)
