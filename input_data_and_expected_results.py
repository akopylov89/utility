#! /usr/bin/python
"""Unit tests input data and expected results"""

import argparse
from collections import OrderedDict
from measurement_result_builder import ResultBuilderWithExecutionExitCode

IPERF_MODE = True
COMMAND = ['command']
IPERF_PORT = '22'
SERVER_IP = '192.168.1.1'
SERVER_HOST = 'server'
TIME = '30'
INTERVAL = '5'
OK_MESSAGE = ''
ERROR_MESSAGE = 'Error!'
ERROR_MESSAGE_HOST1 = "connect failed: No route to host\n"
ERROR_MESSAGE_HOST2 = "connect failed: Connection refused\n"
OK_RETURN_CODE = 0
ERROR_RETURN_CODE = 1
SERVER_USER = 'root'
SERVER_PASSWORD = 'QWERTY'
PASSWORD_FILE = 'file.txt'
OUTPUT_RESULT = """
Client connecting to 192.168.1.1, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  3] local 192.168.2.2 port 42780 connected with 192.168.1.1 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec  2.57 GBytes  2.21 Gbits/sec
0
"""
EXPECTED_IP = {'client ip': '192.168.2.2', 'server ip': '192.168.1.1'}
IPERF_PARSER_EXPECTED_RESULT = OrderedDict([('Total result:',
                                           {'Transfer': '2.57 GBytes',
                                            'Bandwidth': '2.21 Gbits/sec',
                                            'Interval': '0.0-10.0 sec'})])
OUTPUT_RESULT_UDP = """
Client connecting to 192.168.1.1, UDP port 5001
Sending 1470 byte datagrams
UDP buffer size:  208 KByte (default)
------------------------------------------------------------
[  3] local 192.168.2.2 port 55190 connected with 192.168.1.1 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 5.0 sec   640 KBytes  1.05 Mbits/sec
[  3]  5.0-10.0 sec   640 KBytes  1.05 Mbits/sec
[  3]  0.0-10.0 sec  1.25 MBytes  1.05 Mbits/sec
[  3] Sent 1785 datagrams
[  3] Server Report:
[  3]  0.0-10.0 sec  1.25 MBytes  1.05 Mbits/sec   0.028 ms    0/ 1785 (0%)
"""
PARSER_EXPECTED_RESULT2 = OrderedDict([('Time interval 1: 0.0- 5.0 sec',
                                        {'Transfer': '640 KBytes',
                                         'Bandwidth': '1.05 Mbits/sec',
                                         'Interval': '0.0- 5.0 sec'}),
                                       ('Time interval 2: 5.0-10.0 sec',
                                        {'Transfer': '640 KBytes',
                                         'Bandwidth': '1.05 Mbits/sec',
                                         'Interval': '5.0-10.0 sec'}),
                                       ('Time interval 3: 0.0-10.0 sec',
                                        {'Transfer': '1.25 MBytes',
                                         'Bandwidth': '1.05 Mbits/sec',
                                         'Interval': '0.0-10.0 sec'}),
                                       ('Total result:',
                                        {'Transfer': '1.25 MBytes',
                                         'Bandwidth': '1.05 Mbits/sec',
                                         'Interval': '0.0-10.0 sec'})])
EXPECTED_OUTPUT_BUILDER_RESULT = """{
    "error": "",
    "result": {
        "Total result:": {
            "Bandwidth": "2.21 Gbits/sec",
            "Interval": "0.0-10.0 sec",
            "Transfer": "2.57 GBytes"
        }
    },
    "status": 0
}"""
EXPECTED_OUTPUT_BUILDER_ERROR = """{
    "error": "Error!",
    "result": null,
    "status": 1
}"""
EXECUTE_EXPECTED_RESULT =\
    ("\nClient connecting to 192.168.1.1, TCP port 5001\n"
     "TCP window size: 85.0 KByte (default)\n"
     "------------------------------------------------------------\n"
     "[  3] local 192.168.2.2 port 42780 connected with 192.168.1.1 port 5001"
     "\n"
     "[ ID] Interval       Transfer     Bandwidth\n"
     "[  3]  0.0-10.0 sec  2.57 GBytes  2.21 Gbits/sec\n"
     "0\n")

ARGS_INPUT = argparse.Namespace(
            client_host=None, client_ip='192.168.56.101',
            client_password='222222', client_username='root',
            file_client_password=None, file_server_password=None,
            interval=None, port=None, server_host=None,
            server_ip='192.168.56.100', server_password='111111',
            server_username='root', time=None, udp=False)

CONNECTION1 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 OK_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION2 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 OK_MESSAGE,
                                                 ERROR_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION3 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 OK_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 ERROR_RETURN_CODE)
CONNECTION4 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION5 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE_HOST2,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION6 = ResultBuilderWithExecutionExitCode(IPERF_PARSER_EXPECTED_RESULT,
                                                 ERROR_MESSAGE_HOST2,
                                                 OK_RETURN_CODE,
                                                 OK_RETURN_CODE)
CONNECTION_KILL = ResultBuilderWithExecutionExitCode(OK_RETURN_CODE,
                                                     OK_MESSAGE,
                                                     OK_RETURN_CODE,
                                                     OK_MESSAGE)
