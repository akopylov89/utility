#! /usr/bin/python
"""Module with base class for command execution and class for 'sshpass'"""

import subprocess
from iperf_parser import BaseParser, IperfParser
from measurement_result_builder import ResultBuilder, \
    ResultBuilderWithExecutionExitCode


class BaseCommandExecutor(object):
    """class for command execution"""
    def __init__(self, command_to_execute, class_parser=BaseParser):
        self.command_to_execute = command_to_execute
        self.class_parser = class_parser

    def to_execute(self):
        """input - list, output - shell_output, error message, exitcode"""
        data = subprocess.Popen(self.command_to_execute,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        parsed_output = self.class_parser(output_data).to_parse()
        if return_code == 0:
            return ResultBuilder(parsed_output, str(error), return_code)
        else:
            return ResultBuilder(None, str(error), return_code)


class IperfCommandExecutor(BaseCommandExecutor):
    """class for sshpass command execution with special parser"""
    def __init__(self, command_to_execute):
        super(IperfCommandExecutor, self).__init__(command_to_execute,
                                                   class_parser=IperfParser)

    def to_execute(self):
        """input - list, output - shell_output, error message, exitcode"""
        data = subprocess.Popen(self.command_to_execute,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output_data, error = data.communicate()
        return_code = data.returncode
        if output_data:
            return_code_of_execution = int(output_data.split()[-1])
        else:
            return_code_of_execution = 0
        parsed_output = self.class_parser(output_data).to_parse()
        if return_code == 0:
            return ResultBuilderWithExecutionExitCode(parsed_output,
                                                      str(error),
                                                      return_code,
                                                      return_code_of_execution)
        else:
            return ResultBuilderWithExecutionExitCode(None,
                                                      str(error),
                                                      return_code,
                                                      return_code_of_execution)
