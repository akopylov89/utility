# def main():
#     """Main executable function with connection to the first remote host to
#     establish a server, to the second remote host - to establish a client and
#     generate traffic, and finally - to the first host to kill iperf process"""
#     args = parse_command_line_args()
#     final_output = None
#     try:
#         # building iperf command for server host
#         iperf_server_command = IperfServerCommandBuilder()\
#             .set_as_daemon()\
#             .set_mode_udp(args.udp)\
#             .set_port(args.port)\
#             .build_server_command()
#         # building full command of connection to a remote server
#         # and execute iperf command
#         command_to_server = SshCommandBuilder(args.server_username,
#                                               iperf_server_command)\
#             .set_password(args.server_password)\
#             .set_file(args.file_server_password)\
#             .set_ip_address(args.server_ip)\
#             .set_hostname(args.server_host)\
#             .to_build()
#         print 'Connection to server. Please wait ...'
#         # connection to remote host to establish a server(to discard traffic)
#         server_output = BaseCommandExecutor(command_to_server).to_execute()
#         print "Connection to server: exitcode {}, error message '{}' " \
#             .format(server_output.exit_code, server_output.error)
#
#     except KeyboardInterrupt:
#         error_exit_code = 1
#         final_output = ResultBuilder(None, 'Keyboard interruption',
#                                      error_exit_code)
#     except Exception as err:
#         error_exit_code = 2
#         final_output = ResultBuilder(None, str(err), error_exit_code)
#
#     else:
#         # building iperf command for client host
#         iperf_client_command = IperfClientCommandBuilder() \
#             .set_server_ip(args.server_ip) \
#             .set_server_hostname(args.server_host) \
#             .set_mode_udp(args.udp) \
#             .set_port(args.port) \
#             .set_testing_time(args.time) \
#             .set_time_interval(args.interval) \
#             .build_client_command()
#         # building full command of connection to a remote client
#         # and execute iperf command for client
#         command_to_client = SshCommandBuilder(args.client_username,
#                                               iperf_client_command)\
#             .set_password(args.client_password) \
#             .set_file(args.file_client_password) \
#             .set_ip_address(args.client_ip) \
#             .set_hostname(args.client_host) \
#             .to_build()
#         print 'Connection to client. Please wait ...'
#         # connection to remote host to establish a client(to generate traffic)
#         final_output = ClientCommandExecutor(command_to_client).to_execute()
#         print "Connection to client: exitcode {}, error message '{}' " \
#             .format(final_output.exit_code, final_output.error)
#
#     finally:
#         # building full command of connection to a remote server
#         # and execute iperf  killing command
#         command_to_kill = IperfKillCommandBuilder(args.server_username)\
#             .set_password(args.server_password)\
#             .set_file(args.file_server_password)\
#             .set_ip_address(args.server_ip)\
#             .set_hostname(args.server_host)\
#             .to_build()
#         print "Finishing 'iperf' utility on a remote server. " \
#               "Please wait ..."
#         # connection to server to execute iperf killing command
#         connection_to_kill_iperf = BaseCommandExecutor(command_to_kill)\
#             .to_execute()
#         if connection_to_kill_iperf.exit_code:
#             print "Iperf utility is not killed on server"
#         # the result of measurement is printed
#         print "The result of bandwidth measurement is: \n {}" \
#             .format(final_output.build_json())

a = """Filesystem           Size  Used Avail Use% Mounted on
/dev/mapper/cl-root  6.2G  1.1G  5.1G  18% /
devtmpfs             486M     0  486M   0% /dev
tmpfs                497M     0  497M   0% /dev/shm
tmpfs                497M  6.6M  490M   2% /run
tmpfs                497M     0  497M   0% /sys/fs/cgroup
/dev/sda1           1014M  138M  877M  14% /boot
tmpfs                100M     0  100M   0% /run/user/0
0"""

b = a.splitlines()
print b[-1]



# class MyError(Exception):
#     def __init__(self, message, return_code):
#         self.message = message
#         self.return_code = return_code
#
# keyboard_interrupt_error = 100
# iperf_killing_error = 101
# server_firewall_error = 102
# other_errors = 255
#
#
# def connection_to_server():
#     args = parse_command_line_args()
#     # building iperf command for server host
#     iperf_server_command = IperfServerCommandBuilder()\
#         .set_as_daemon()\
#         .set_mode_udp(args.udp)\
#         .set_port(args.port)\
#         .set_checking_of_execution()\
#         .build_server_command()
#     # building full command of connection to a remote server
#     # and execute iperf command
#     command_to_server = SshCommandBuilder(args.server_username,
#                                           iperf_server_command)\
#         .set_password(args.server_password)\
#         .set_file(args.file_server_password)\
#         .set_ip_address(args.server_ip)\
#         .set_hostname(args.server_host)\
#         .to_build()
#     print 'Connection to server. Please wait ...'
#     # connection to remote host to establish a server(to discard traffic)
#     result = BaseCommandExecutor(command_to_server).to_execute()
#     error_exit_code = 0
#     if result.exit_code:
#         error_exit_code = result.exit_code
#         raise MyError(result.error, error_exit_code)
#     exit_code_of_exec_command = int(result.output.split()[-1])
#     if exit_code_of_exec_command:
#         error_exit_code = exit_code_of_exec_command
#         raise MyError("Iperf server establishing error", error_exit_code)
#     return error_exit_code
#
#
# def connection_to_client():
#     args = parse_command_line_args()
#     # building iperf command for client host
#     iperf_client_command = IperfClientCommandBuilder() \
#         .set_server_ip(args.server_ip) \
#         .set_server_hostname(args.server_host) \
#         .set_mode_udp(args.udp) \
#         .set_port(args.port) \
#         .set_testing_time(args.time) \
#         .set_time_interval(args.interval) \
#         .build_client_command()
#     # building full command of connection to a remote client
#     # and execute iperf command for client
#     command_to_client = SshCommandBuilder(args.client_username,
#                                           iperf_client_command)\
#         .set_password(args.client_password) \
#         .set_file(args.file_client_password) \
#         .set_ip_address(args.client_ip) \
#         .set_hostname(args.client_host) \
#         .to_build()
#     print 'Connection to client. Please wait ...'
#     # connection to remote host to establish a client(to generate traffic)
#     result = ClientCommandExecutor(command_to_client).to_execute()
#     if result.exit_code:
#         raise MyError(result.error, result.exit_code)
#     if result.error == "connect failed: No route to host\n":
#         error_exit_code = server_firewall_error
#         raise MyError(result.error, error_exit_code)
#     return result
#
#
# def connection_to_server_to_kill_iperf():
#     args = parse_command_line_args()
#     # building full command of connection to a remote server
#     # and execute iperf  killing command
#     command_to_kill = IperfKillCommandBuilder(args.server_username)\
#         .set_password(args.server_password)\
#         .set_file(args.file_server_password)\
#         .set_ip_address(args.server_ip)\
#         .set_hostname(args.server_host)\
#         .to_build()
#     print "Finishing 'iperf' utility on a remote server. " \
#           "Please wait ..."
#     # connection to server to execute iperf killing command
#     result = BaseCommandExecutor(command_to_kill).to_execute()
#     return result
#
#
# if __name__ == "__main__":
#     try:
#         connection_to_server = connection_to_server()
#         if not connection_to_server:
#             connection_to_client = connection_to_client()
#             print "The result of bandwidth measurement is: \n {}" \
#                 .format(connection_to_client.build_json())
#
#     except KeyboardInterrupt:
#         output = ResultBuilder(None, 'Keyboard interruption',
#                                keyboard_interrupt_error)
#         print output.build_json()
#         sys.exit(keyboard_interrupt_error)
#
#     except MyError as err:
#         output = ResultBuilder(None, err.message, err.return_code)
#         print output.build_json()
#         sys.exit(err.return_code)
#
#     except Exception as err:
#         output = ResultBuilder(None, str(err), other_errors)
#         print output.build_json()
#         sys.exit(other_errors)
#
#     finally:
#         finishing_result = connection_to_server_to_kill_iperf()
#         if finishing_result.exit_code:
#             print "Iperf is not killed on server"
#             sys.exit(iperf_killing_error)

def parse_command_line_args():
    """function to parse command line arguments"""
    parser = argparse.ArgumentParser(
        prog='bandwidth_measurement_utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Command line utility for performing network throughput
        measurements.  It can test either TCP or UDP throughput.  To perform
        a test  the  user must  establish  both  a  server  (to discard
        traffic) and a client (to generate traffic).
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
        102     Ssh connection error
        103     Server firewall error
        104     Server establishing error
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


def connection_to_server():
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


def connection_to_client():
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
        connection_to_server = connection_to_server()

        # checking if sshpass error occurred
        SshpassErrorExitCodeController(connection_to_server.exit_code,
                                       connection_to_server.error)\
            .check_if_error()
        # checking if ssh error occurred
        SshErrorExitCodeController(connection_to_server.exit_code,
                                   connection_to_server.error)\
            .check_if_error()

        # checking if error of executable command occurred on a remote host
        ExecutionExitCodeController(connection_to_server.exit_code_execution,
                                    connection_to_server.error)\
            .check_if_error()

        # checking if other errors occurred
        OtherErrorsChecking(connection_to_server.exit_code,
                            connection_to_server.error)\
            .check_if_error()

        # connection to client
        connection_to_client = connection_to_client()
        # checking if sshpass error occurred
        SshpassErrorExitCodeController(connection_to_client.exit_code,
                                       connection_to_client.error) \
            .check_if_error()
        # checking if ssh error occurred
        SshErrorExitCodeController(connection_to_client.exit_code,
                                   connection_to_client.error) \
            .check_if_error()
        # checking if error of executable command occurred on a remote host
        ExecutionExitCodeController(connection_to_client.exit_code_execution,
                                    connection_to_client.error) \
            .check_if_error()
        # checking if other errors occurred
        OtherErrorsChecking(connection_to_client.exit_code,
                            connection_to_client.error) \
            .check_if_error()
        print "The result of bandwidth measurement is: \n {}" \
            .format(connection_to_client.build_json())

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








class TestConnectionToServer(unittest.TestCase):
    """unit tests for connection_to_server() function"""
    def test_correct_connection(self):
        """testing of connection without any error"""
        result = ResultBuilderWithExecutionExitCode(OUTPUT_RESULT,
                                                    OK_MESSAGE,
                                                    255,
                                                    OK_RETURN_CODE)
        with patch('bandwidth_measurement_utility.connection_to_server',
                   return_value=result) \
                as mock_connect:
            error_checking_decorator(mock_connect())