#! /usr/bin/python
"""Command line utility for bandwidth measurement between two remote hosts"""

import sys
import argparse
import textwrap
from sshpass_command_builder import SshCommandBuilder, IperfKillCommandBuilder
from iperf_command_builder import IperfServerCommandBuilder, \
    IperfClientCommandBuilder
from command_executor import IperfCommandExecutor
from error_check import MyError, SshpassErrorExitCodeController, \
    SshErrorExitCodeController, ExecutionExitCodeController, \
    OtherErrorsChecking


def parse_command_line_args():
    """function to parse command line arguments"""
    parser = argparse.ArgumentParser(
        prog='bandwidth_measurement_utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Command line utility for performing network throughput
        measurements.  It can test either TCP or UDP throughput.
        To perform a test  the  user must  establish  both  a
        server  (to discard traffic) and a client (to generate
        traffic).
        RETURN VALUES
        As  with  any  other  program, this utility returns 0 on success.
        In case of failure, the following return codes are used:
        1       Invalid command line argument
        2       Conflicting arguments given
        3       General runtime error
        4       Unrecognized response from ssh (parse error)
        5       Invalid/incorrect password
        6       Host public key is unknown. sshpass exits without confirming
                the new key
        100     Keyboard interruption
        101     Remote host command execution error
        102     Server firewall error
        103     Server establishing error
        255     Ssh connection error
        """))
    # only one of server ip and server hostname is required
    group_server_address = parser.add_mutually_exclusive_group(required=True)
    # only one of client ip and client hostname is required
    group_client_address = parser.add_mutually_exclusive_group(required=True)
    # only one of server password and file with server password is required
    group_server_password = parser.add_mutually_exclusive_group(required=True)
    # only one of client password and file with client password is required
    group_client_password = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-s_user', '--server_username', required=True,
                        help='Username of a remote host used as server')
    parser.add_argument('-cl_user', '--client_username', required=True,
                        help='Username of a remote host used as client')
    group_server_address.add_argument('-s_ip', '--server_ip',
                                      help='IP address fo a remote host used '
                                           'as server')
    group_server_address.add_argument('-s_host', '--server_host',
                                      help='Hostname of a remote host used '
                                           'as server')
    group_client_address.add_argument('-cl_ip', '--client_ip',
                                      help='IP address of a remote host used '
                                           'as client')
    group_client_address.add_argument('-cl_host', '--client_host',
                                      help='Hostname of a remote host used '
                                           'as client')
    group_server_password.add_argument('-s_password', '--server_password',
                                       help='Password of a remote host used '
                                            'as server')
    group_server_password.add_argument('-s_file', '--file_server_password',
                                       help='File with password of a remote '
                                            'host used as server')
    group_client_password.add_argument('-cl_password', '--client_password',
                                       help='Password of a remote host used '
                                            'as client')
    group_client_password.add_argument('-cl_file', '--file_client_password',
                                       help='File with password of a remote '
                                            'host used as client')
    parser.add_argument('-u', '--udp', action='store_true', default=False,
                        help='Use UDP rather than TCP')
    parser.add_argument('-port', '--port',
                        help='Set server port to listen on and client to '
                             'connect to')
    parser.add_argument('-time', '--time',
                        help='Time in seconds to transmit for')
    parser.add_argument('-interval', '--interval',
                        help='Pause n seconds between periodic bandwidth '
                             'reports')
    args = parser.parse_args()
    return args


def error_checking_decorator(func):
    """decorator to check exit codes of connections to remote hosts"""
    def check_if_error():
        result = func()
        SshpassErrorExitCodeController(result.exit_code, result.error) \
            .check_if_error()
        # checking if ssh error occurred
        SshErrorExitCodeController(result.exit_code, result.error) \
            .check_if_error()
        # checking if error of executable command occurred on a remote host
        ExecutionExitCodeController(result.exit_code_execution, result.error) \
            .check_if_error()
        # checking if other errors occurred
        OtherErrorsChecking(result.exit_code, result.error) \
            .check_if_error()
        return result
    return check_if_error


@error_checking_decorator
def connection_to_server():
    """function to make connection to remote host to establish a server"""
    args = parse_command_line_args()
    # building iperf command for server host
    iperf_server_command = IperfServerCommandBuilder()\
        .set_as_daemon()\
        .set_mode_udp(args.udp)\
        .set_port(args.port)\
        .set_checking_of_execution()\
        .build_server_command()
    # building full command of connection to a remote server
    # and execute iperf command
    command_to_server = SshCommandBuilder(args.server_username,
                                          iperf_server_command)\
        .set_password(args.server_password)\
        .set_file(args.file_server_password)\
        .set_ip_address(args.server_ip)\
        .set_hostname(args.server_host)\
        .to_build()
    print 'Connection to server. Please wait ...'
    # connection to remote host to establish a server(to discard traffic)
    result = IperfCommandExecutor(command_to_server).to_execute()
    return result


@error_checking_decorator
def connection_to_client():
    """function to make connection to remote host to establish a client"""
    args = parse_command_line_args()
    # building iperf command for client host
    iperf_client_command = IperfClientCommandBuilder() \
        .set_server_ip(args.server_ip) \
        .set_server_hostname(args.server_host) \
        .set_mode_udp(args.udp) \
        .set_port(args.port) \
        .set_testing_time(args.time) \
        .set_time_interval(args.interval) \
        .set_checking_of_execution() \
        .build_client_command()
    # building full command of connection to a remote client
    # and execute iperf command for client
    command_to_client = SshCommandBuilder(args.client_username,
                                          iperf_client_command)\
        .set_password(args.client_password) \
        .set_file(args.file_client_password) \
        .set_ip_address(args.client_ip) \
        .set_hostname(args.client_host) \
        .to_build()
    print 'Connection to client. Please wait ...'
    # connection to remote host to establish a client(to generate traffic)
    result = IperfCommandExecutor(command_to_client).to_execute()
    return result


def connection_to_server_to_kill_iperf():
    """function to make connection to server to kill iperf utility"""
    args = parse_command_line_args()
    # building full command of connection to a remote server
    # and execute iperf  killing command
    command_to_kill = IperfKillCommandBuilder(args.server_username)\
        .set_password(args.server_password)\
        .set_file(args.file_server_password)\
        .set_ip_address(args.server_ip)\
        .set_hostname(args.server_host)\
        .to_build()
    print "Finishing 'iperf' utility on a remote server. " \
          "Please wait ..."
    # connection to server to execute iperf killing command
    result = IperfCommandExecutor(command_to_kill).to_execute()
    return result


if __name__ == "__main__":
    parse_command_line_args()
    try:
        # connection to server
        connection_to_establish_server = connection_to_server()

        # connection to client
        connection_to_generate_traffic = connection_to_client()
        print "The result of bandwidth measurement is: \n {}" \
            .format(connection_to_generate_traffic.build_json())

    except KeyboardInterrupt:
        print('Keyboard Interruption')
        sys.exit(100)

    except MyError as err:
        print err.message
        sys.exit(err.return_code)

    finally:
        finishing_result = connection_to_server_to_kill_iperf()
        if finishing_result.exit_code_execution:
            print 'Iperf is not killed on server'
