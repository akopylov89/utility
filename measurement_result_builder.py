#! /usr/bin/python
"""Module with class ResultBuilder for compose in a dict the result
output of command, error message and exit code, and serialize it to
a JSON formatted str"""

import json


class ResultBuilder(object):
    """class to compose the final output and return it as json"""
    def __init__(self, output, error, exit_code):
        self.output = output
        self.error = error
        self.exit_code = exit_code

    def build_json(self):
        """Composing all results of command execution in a dict and
        serializing it to a json format"""
        data_as_dict = {
            'error': str(self.error),
            'result': self.output,
            'status': self.exit_code
        }
        json_data = json.dumps(data_as_dict, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data


class ResultBuilderWithExecutionExitCode(ResultBuilder):
    def __init__(self, output, error, exit_code, exit_code_execution):
        super(ResultBuilderWithExecutionExitCode, self)\
            .__init__(output, error, exit_code)
        self.exit_code_execution = exit_code_execution
