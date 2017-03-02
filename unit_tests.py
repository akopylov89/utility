#! /usr/bin/python
# pylint: disable=R0904
"""Unit tests"""

import unittest
from mock import Mock, patch
from command_executor import BaseCommandExecutor, IperfCommandExecutor
from iperf_command_builder import IperfClientCommandBuilder,\
    IperfServerCommandBuilder, BaseIperfCommandBuilder
from iperf_parser import IperfParser
from measurement_result_builder import ResultBuilder
from sshpass_command_builder import SshCommandBuilder, \
    SshpassBaseCommandBuilder, IperfKillCommandBuilder
from error_check import MyError, BaseErrorExitCodeController, \
    SshpassErrorExitCodeController, SshErrorExitCodeController, \
    ExecutionExitCodeController, OtherErrorsChecking
from input_data_and_expected_results import *
from bandwidth_measurement_utility import connection_to_server, \
    connection_to_client, connection_to_server_to_kill_iperf


class TestBaseIperfCommandBuilder(unittest.TestCase):
    """unit tests for BaseIperfCommandBuilder class"""
    def test_set_mode_udp(self):
        """testing self.mode_udp setter"""
        actual_result = BaseIperfCommandBuilder().set_mode_udp(IPERF_MODE)\
            .mode_udp
        self.assertEqual(actual_result, True)

    def test_set_port(self):
        """testing self.port setter"""
        actual_result = BaseIperfCommandBuilder().set_port(IPERF_PORT).port
        self.assertEqual(actual_result, '22')

    def test_set_checking_of_execution(self):
        """testing self.checking_of_execution setter"""
        actual_result = BaseIperfCommandBuilder()\
            .set_checking_of_execution()\
            .check_of_execution
        self.assertEqual(actual_result, [';echo', '$?'])


class TestIperfServerCommandBuilder(unittest.TestCase):
    """unit tests for IperfServerCommandBuilder class"""

    def test_set_as_daemon(self):
        """testing self.daemon setter"""
        actual_result = IperfServerCommandBuilder().set_as_daemon().daemon
        self.assertEqual(actual_result, '-D')

    def test_build_command(self):
        """testing of 'iperf -s' command building"""
        actual_result = IperfServerCommandBuilder().build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s'])

    def test_build_command_daemon(self):
        """testing of 'iperf -s -D' command building"""
        actual_result = IperfServerCommandBuilder()\
            .set_as_daemon().build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s', '-D'])

    def test_build_command_mode_udp(self):
        """testing of 'iperf -s -D -u' command building"""
        actual_result = IperfServerCommandBuilder()\
            .set_mode_udp(IPERF_MODE)\
            .build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s', '-u'])

    def test_build_command_port(self):
        """testing of 'iperf -s -D -p 22' command building"""
        actual_result = IperfServerCommandBuilder()\
            .set_port(IPERF_PORT)\
            .build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s', '-p', '22'])

    def test_build_command_with_all(self):
        """testing of 'iperf -s -D -u -p 22' command building"""
        actual_result = IperfServerCommandBuilder()\
            .set_port(IPERF_PORT)\
            .set_mode_udp(IPERF_MODE)\
            .set_as_daemon()\
            .set_checking_of_execution()\
            .build_server_command()
        self.assertListEqual(actual_result, ['iperf', '-s', '-D', '-u',
                                             '-p', '22', ';echo', '$?'])


class TestIperfClientCommandBuilder(unittest.TestCase):
    """unit tests for IperfClientCommandBuilder class"""

    def test_set_server_ip(self):
        """testing self.server)ip setter"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_ip(SERVER_IP)\
            .server_ip
        self.assertEqual(actual_result, '192.168.1.1')

    def test_set_server_hostname(self):
        """testing self.server_hostname setter"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_hostname(SERVER_HOST)\
            .server_hostname
        self.assertEqual(actual_result, 'server')

    def test_set_testing_time(self):
        """testing self.testing_time setter"""
        actual_result = IperfClientCommandBuilder() \
            .set_testing_time(TIME).testing_time
        self.assertEqual(actual_result, '30')

    def test_set_time_interval(self):
        """testing self.interval setter"""
        actual_result = IperfClientCommandBuilder() \
            .set_time_interval(INTERVAL).interval
        self.assertEqual(actual_result, '5')

    def test_build_command_daemon(self):
        """testing of 'iperf -c 192.168.1.1' command with daemon
        client building"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_ip(SERVER_IP)\
            .build_client_command()
        self.assertListEqual(actual_result, ['iperf', '-c', '192.168.1.1'])

    def test_build_command_ip(self):
        """testing of 'iperf -c 192.168.1.1' command building"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_ip(SERVER_IP)\
            .build_client_command()
        self.assertListEqual(actual_result, ['iperf', '-c', '192.168.1.1'])

    def test_build_command_hostname(self):
        """testing of 'iperf -c server' command building"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_hostname(SERVER_HOST)\
            .build_client_command()
        self.assertListEqual(actual_result, ['iperf', '-c', 'server'])

    def test_exception_raise(self):
        """testing of 'iperf -c' command error raising"""
        with self.assertRaises(Exception):
            IperfClientCommandBuilder().build_client_command()

    def test_exception_raise2(self):
        """testing of 'iperf -c' command error raising"""
        with self.assertRaises(Exception):
            IperfClientCommandBuilder()\
                .set_server_ip(SERVER_IP)\
                .set_server_hostname(SERVER_HOST)\
                .build_client_command()

    def test_build_command_testing_time(self):
        """testing of 'iperf -c server -t 30' command building"""
        actual_result = IperfClientCommandBuilder()\
            .set_server_hostname(SERVER_HOST)\
            .set_testing_time(TIME)\
            .build_client_command()
        self.assertListEqual(actual_result,
                             ['iperf', '-c', 'server', '-t', '30'])

    def test_time_interval(self):
        """testing of 'iperf -c server -i 5' command building"""
        actual_result = IperfClientCommandBuilder() \
            .set_server_hostname(SERVER_HOST) \
            .set_time_interval(INTERVAL) \
            .build_client_command()
        self.assertListEqual(actual_result,
                             ['iperf', '-c', 'server', '-i', '5'])

    def test_build_full_command(self):
        """testing of 'iperf -c 192.168.1.1 -u -p 22 -t 30 -i 5'
        command building"""
        actual_result = IperfClientCommandBuilder() \
            .set_server_ip(SERVER_IP)\
            .set_port('22')\
            .set_mode_udp(IPERF_MODE)\
            .set_time_interval(INTERVAL)\
            .set_testing_time(TIME) \
            .build_client_command()
        self.assertListEqual(actual_result,
                             ['iperf', '-c', '192.168.1.1', '-u',
                              '-p', '22', '-t', '30', '-i', '5'])


class TestParser(unittest.TestCase):
    """unit tests for class IperfParser"""

    def test_string_to_dict(self):
        """testing of correct transformation of string to dict"""
        actual_result = IperfParser(OUTPUT_RESULT).to_parse()
        self.assertEqual(actual_result, IPERF_PARSER_EXPECTED_RESULT)

    def test_string_to_dict2(self):
        """testing of correct transformation of string to dict"""
        actual_result = IperfParser(OUTPUT_RESULT_UDP).to_parse()
        self.assertEqual(actual_result, PARSER_EXPECTED_RESULT2)


class TestResultBuilder(unittest.TestCase):
    """unit tests for class ResultBuilder"""
    def test_to_json(self):
        """testing of correct output in json"""
        actual_result = ResultBuilder(IPERF_PARSER_EXPECTED_RESULT,
                                      OK_MESSAGE,
                                      OK_RETURN_CODE).build_json()
        self.assertMultiLineEqual(actual_result,
                                  EXPECTED_OUTPUT_BUILDER_RESULT)

    def test_to_json_with_non_result(self):
        """testing of correct output in json when there is no result,
        message about error and error returncode"""
        actual_result = ResultBuilder(None,
                                      ERROR_MESSAGE,
                                      ERROR_RETURN_CODE).build_json()
        self.assertMultiLineEqual(actual_result, EXPECTED_OUTPUT_BUILDER_ERROR)


class TestBaseCommandExecutor(unittest.TestCase):
    """unit test for class BaseCommandExecutor"""
    def test_execute(self):
        """testing of correct output of bandwidth measurements"""
        with patch('command_executor.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (OUTPUT_RESULT,
                                                  OK_MESSAGE),
                     'returncode': OK_RETURN_CODE}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = BaseCommandExecutor(COMMAND).to_execute()
            self.assertIs(actual_result.error, OK_MESSAGE)
            self.assertIs(actual_result.exit_code, OK_RETURN_CODE)
            self.assertMultiLineEqual(actual_result.output,
                                      EXECUTE_EXPECTED_RESULT)


class TestClientCommandExecutor(unittest.TestCase):
    """unit test for class ClientCommandExecutor"""
    def test_execute(self):
        """testing of correct output of bandwidth measurements"""
        with patch('command_executor.subprocess.Popen') as mock_subproc_popen:
            communicate_mock = Mock()
            attrs = {'communicate.return_value': (OUTPUT_RESULT,
                                                  OK_MESSAGE),
                     'returncode': OK_RETURN_CODE}
            communicate_mock.configure_mock(**attrs)
            mock_subproc_popen.return_value = communicate_mock
            actual_result = IperfCommandExecutor(COMMAND).to_execute()
            self.assertIs(actual_result.error, OK_MESSAGE)
            self.assertIs(actual_result.exit_code, OK_RETURN_CODE)
            self.assertDictEqual(actual_result.output,
                                 IPERF_PARSER_EXPECTED_RESULT)


class TestIperfKillCommandBuilder(unittest.TestCase):
    """unit test for class IperfKillCommandBuilder"""
    def test_build_kill_command(self):
        """testing iperf killing command building"""
        actual_result = IperfKillCommandBuilder(SERVER_USER)\
            .set_ip_address(SERVER_IP)\
            .set_password(SERVER_PASSWORD)\
            .to_build()
        self.assertListEqual(actual_result,
                             ['sshpass', '-p', 'QWERTY', 'ssh',
                              'root@192.168.1.1', 'pkill', '-9',
                              'iperf', ';echo', '$?'])


class TestSshpassBaseCommandBuilder(unittest.TestCase):
    """unit tests for SshpassBaseCommandBuilder class"""
    def test_set_password(self):
        """testing self.password setter"""
        actual_result = SshpassBaseCommandBuilder(COMMAND) \
            .set_password(SERVER_PASSWORD).password
        self.assertEqual(actual_result, 'QWERTY')

    def test_set_password_file(self):
        """testing self.password_file setter"""
        actual_result = SshpassBaseCommandBuilder(COMMAND) \
            .set_file(PASSWORD_FILE).password_file
        self.assertEqual(actual_result, 'file.txt')

    def test_raise_exception(self):
        """testing of error raising if neither password no file are set"""
        with self.assertRaises(Exception):
            SshpassBaseCommandBuilder(COMMAND).to_build()

    def test_raise_exception2(self):
        """testing of error raising if both password and file are set"""
        with self.assertRaises(Exception):
            SshpassBaseCommandBuilder(COMMAND)\
                .set_password(SERVER_PASSWORD)\
                .set_file(PASSWORD_FILE)\
                .to_build()

    def test_build_command_password(self):
        """testing of 'sshpass -p password command' building"""
        actual_result = SshpassBaseCommandBuilder(COMMAND)\
            .set_password(SERVER_PASSWORD)\
            .to_build()
        self.assertListEqual(actual_result,
                             ['sshpass', '-p', 'QWERTY', 'command'])

    def test_build_command_file(self):
        """testing of 'sshpass -f file.txt command' building"""
        actual_result = SshpassBaseCommandBuilder(COMMAND) \
            .set_file(PASSWORD_FILE) \
            .to_build()
        self.assertListEqual(actual_result,
                             ['sshpass', '-f', 'file.txt', 'command'])


class TestSshCommandBuilder(unittest.TestCase):
    """unit tests for SshCommandBuilder class"""
    def test_set_ip_address(self):
        """testing self.ip_address setter"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND)\
            .set_ip_address(SERVER_IP)\
            .ip_address
        self.assertEqual(actual_result, '192.168.1.1')

    def test_set_hostname(self):
        """testing self.hostname setter"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND)\
            .set_hostname(SERVER_HOST)\
            .hostname
        self.assertEqual(actual_result, 'server')

    def test_raise_exception(self):
        """testing of error raising if neither ip address no
        hostname are set"""
        with self.assertRaises(Exception):
            SshCommandBuilder(SERVER_USER, COMMAND).to_build()

    def test_raise_exception2(self):
        """testing of error raising if both ip address and
        hostname are set"""
        with self.assertRaises(Exception):
            SshCommandBuilder(SERVER_USER, COMMAND)\
                .set_ip_address(SERVER_IP)\
                .set_hostname(SERVER_HOST)\
                .to_build()

    def test_build_ssh_ip_command(self):
        """testing of 'sshpass -p password ssh root@192.168.1.1 command'
        building"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND) \
            .set_password(SERVER_PASSWORD) \
            .set_ip_address(SERVER_IP) \
            .to_build()
        self.assertListEqual(actual_result,
                             ['sshpass', '-p', 'QWERTY', 'ssh',
                              'root@192.168.1.1', 'command'])

    def test_build_ssh_hostname_command(self):
        """testing of 'sshpass -p password ssh root@server command'
        building"""
        actual_result = SshCommandBuilder(SERVER_USER, COMMAND) \
            .set_password(SERVER_PASSWORD) \
            .set_hostname(SERVER_HOST) \
            .to_build()
        self.assertListEqual(actual_result,
                             ['sshpass', '-p', 'QWERTY', 'ssh',
                              'root@server', 'command'])


class TestBaseErrorExitCodeController(unittest.TestCase):
    """unit tests for BaseErrorExitCodeController class"""
    def test_check_if_error(self):
        """testing of error occurring if exit code is not 0"""
        with self.assertRaises(MyError):
            BaseErrorExitCodeController(ERROR_RETURN_CODE, ERROR_MESSAGE)\
                .check_if_error()

    def test_check_if_not_error(self):
        """testing of error not occurring if exit code is 0"""
        actual_result = BaseErrorExitCodeController(OK_RETURN_CODE,
                                                    OK_MESSAGE)\
            .check_if_error()
        self.assertIsNone(actual_result)


class TestSshpassErrorExitCodeController(unittest.TestCase):
    """unit tests for SshpassErrorExitCodeController class"""
    def test_check_if_error_one(self):
        """testing of error occurring if exit code is 1"""
        with self.assertRaises(MyError):
            SshpassErrorExitCodeController(ERROR_RETURN_CODE, ERROR_MESSAGE)\
                .check_if_error()

    def test_check_if_error_six(self):
        """testing of error occurring if exit code is 6"""
        with self.assertRaises(MyError):
            SshpassErrorExitCodeController(6, ERROR_MESSAGE)\
                .check_if_error()

    def test_check_if_not_error(self):
        """testing of error not occurring if exit code is 0"""
        actual_result = SshpassErrorExitCodeController(OK_RETURN_CODE,
                                                       OK_MESSAGE)\
            .check_if_error()
        self.assertIsNone(actual_result)


class TestSshErrorExitCodeController(unittest.TestCase):
    """unit tests for SshErrorExitCodeController class"""
    def test_check_if_error(self):
        """testing of error occurring if exit code is 255"""
        with self.assertRaises(MyError):
            SshErrorExitCodeController(255, ERROR_MESSAGE)\
                .check_if_error()

    def test_check_if_not_error(self):
        """testing of error not occurring if exit code is 0"""
        actual_result = SshErrorExitCodeController(OK_RETURN_CODE,
                                                   OK_MESSAGE)\
            .check_if_error()
        self.assertIsNone(actual_result)


class TestExecutionExitCodeController(unittest.TestCase):
    """unit tests for ExecutionExitCodeController class"""
    def test_check_if_error(self):
        """testing of error occurring if exit code is not 0"""
        with self.assertRaises(MyError):
            ExecutionExitCodeController(ERROR_RETURN_CODE, ERROR_MESSAGE)\
                .check_if_error()

    def test_check_if_not_error(self):
        """testing of error not occurring if exit code is 0 and message
        is empty"""
        actual_result = ExecutionExitCodeController(OK_RETURN_CODE,
                                                    OK_MESSAGE)\
            .check_if_error()
        self.assertIsNone(actual_result)

    def test_check_if_error_message(self):
        """testing of error occurring if error message is not empty"""
        with self.assertRaises(MyError):
            ExecutionExitCodeController(OK_RETURN_CODE, ERROR_MESSAGE)\
                .check_if_error()


class TestOtherErrorsChecking(unittest.TestCase):
    """unit tests for OtherErrorsChecking class"""
    def test_check_if_error_one(self):
        """testing of error occurring if error message is
        'connect failed: No route to host\n'"""
        with self.assertRaises(MyError):
            OtherErrorsChecking(OK_RETURN_CODE, ERROR_MESSAGE_HOST1)\
                .check_if_error()

    def test_check_if_error_two(self):
        """testing of error occurring if error message is
        'connect failed: Connection refused\n'"""
        with self.assertRaises(MyError):
            OtherErrorsChecking(OK_RETURN_CODE, ERROR_MESSAGE_HOST2) \
                .check_if_error()

    def test_check_if_not_error(self):
        """testing of error not occurring if error message is 'Error!'"""
        actual_result = SshErrorExitCodeController(ERROR_RETURN_CODE,
                                                   OK_MESSAGE)\
            .check_if_error()
        self.assertIsNone(actual_result)


class TestConnectionToServer(unittest.TestCase):
    """unit tests for connection_to_server() function"""
    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_correct_connectiom(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION1
        mock_execute.return_value = result
        actual_result = connection_to_server()
        self.assertIs(actual_result.error, "")
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.exit_code_execution, 0)
        self.assertIs(actual_result.output, IPERF_PARSER_EXPECTED_RESULT)

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_error(self, mock_execute, mock_parse):
        """testing of error occurring if exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION2
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_error_execute(self, mock_execute, mock_parse):
        """testing of error occurring if execution exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION3
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error(self, mock_execute, mock_parse):
        """testing of error not occurring if error message is 'Error!'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION4
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_server()


class TestConnectionToClient(unittest.TestCase):
    """unit tests for connection_to_client() function"""
    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_correct_connection(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION1
        mock_execute.return_value = result
        actual_result = connection_to_client()
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.error, "")
        self.assertIs(actual_result.exit_code_execution, 0)
        self.assertIs(actual_result.output, IPERF_PARSER_EXPECTED_RESULT)

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_error(self, mock_execute, mock_parse):
        """testing of error occurring if exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION2
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_error_execute(self, mock_execute, mock_parse):
        """testing of error occurring if execution exit code is not 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION3
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error(self, mock_execute, mock_parse):
        """testing of error not occurring if error message is 'Error!'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION4
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error_and_no_exit(self, mock_execute,
                                                         mock_parse):
        """testing of error occurring if error message is
        'connect failed: No route to host\n'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION5
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()

    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_connection_raises_message_error_and_no_exit2(self, mock_execute,
                                                          mock_parse):
        """testing of error occurring if error message is
        'connect failed: Connection refused\n'"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION6
        mock_execute.return_value = result
        with self.assertRaises(MyError):
            connection_to_client()


class TestConnectionToKillIperf(unittest.TestCase):
    """unit tests for connection_to_server_to_kill_iperf() function"""
    @patch('bandwidth_measurement_utility.parse_command_line_args')
    @patch('bandwidth_measurement_utility.IperfCommandExecutor.to_execute')
    def test_correct_connection(self, mock_execute, mock_parse):
        """testing of error not occurring if exit code is 0"""
        mock_parse.return_value = ARGS_INPUT
        result = CONNECTION_KILL
        mock_execute.return_value = result
        actual_result = connection_to_server_to_kill_iperf()
        self.assertIs(actual_result.exit_code, 0)
        self.assertIs(actual_result.error, '')
        self.assertIs(actual_result.exit_code_execution, '')
        self.assertIs(actual_result.output, 0)


if __name__ == '__main__':
    unittest.main()
