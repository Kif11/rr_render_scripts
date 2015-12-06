import SocketServer
import time
import sys
import os
import traceback
import datetime
import struct
import socket
parent_dir = os.path.join(os.getcwd(), '..')
sys.path.append(parent_dir)
from utils.logger import Logger


STRUCTURE_ID_RRCOMMANDS  = 0x0B03
STRUCTURE_ID_RRN_TCP_HEADER_DATA_V3 = 0x0D03
SIZE_RRCOMMANDS = 1232
SIZE_RRN_TCP_HEADERDATA_V3 = 198
RRNDATA_COMMANDS = 7
COMMAND_TIMEOUT = 180

class _RRCommands(object):

    def __init__(self):
        self.PACK_FORMAT = '=HBBhbbQii1002sHH200?bb'
        self.structure_id = STRUCTURE_ID_RRCOMMANDS
        self.ctype = 4
        self.command = 0
        self.param_id = 0
        self.param_x = 0
        self.param_y = 0
        self.param_s = ''
        self.param_slength = 0
        self.param_stype = 0

    def to_binary(self):
        keptfree = 0
        return struct.pack(self.PACK_FORMAT, self.structure_id, self.ctype,
                           self.command, keptfree, keptfree,keptfree, self.param_id,
                           self.param_x, self.param_y, keptfree, keptfree,
                           self.param_s, self.param_slength, self.param_stype)

    def from_binary(self, buf):
        tmp = struct.unpack(self.PACK_FORMAT, buf)
        self.structure_id = tmp[0]
        self.ctype = tmp[1]
        self.command = tmp[2]
        self.param_id = tmp[6]
        self.param_x = tmp[7]
        self.param_y = tmp[8]
        params_temp =tmp[9]
        self.param_slength = tmp[10]
        self.param_stype = tmp[11]
        self.param_s = ''

        # TODO(Holger): String is actually unicode 16bit,
        # but for now a dirty ANSI conversion is fine
        for c in range(0, self.param_slength):
            self.param_s = self.param_s + params_temp[c * 2]

    def is_right_struct(self):
        return self.structure_id == STRUCTURE_ID_RRCOMMANDS


class _RRN_TCP_HeaderData_v3(object):

    def __init__(self):
        self.PACK_FORMAT = '=HIIHbhB182s'
        self.structure_id = STRUCTURE_ID_RRN_TCP_HEADER_DATA_V3
        data_length = 0
        data_type = 0
        data_nrelements = 0
        self.app_type=14

    def to_binary(self):
        keptfree = 0
        keptfreeS = ""
        return struct.pack(self.PACK_FORMAT, STRUCTURE_ID_RRN_TCP_HEADER_DATA_V3,
                           keptfree,self.data_length, keptfree, self.data_type,
                           self.data_nrelements, self.app_type, keptfreeS)

    def from_binary(self, buf):
        tmp = struct.unpack(self.PACK_FORMAT, buf)
        self.structure_id = tmp[0]
        self.data_length = tmp[2]
        self.data_type = tmp[4]
        self.data_nrelements= tmp[5]
        self.app_type = tmp[6]

    def is_right_struct(self):
        return self.structure_id == STRUCTURE_ID_RRN_TCP_HEADER_DATA_V3


class rrKSOTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        """
        Method for processing incoming requests.
        This overide handle method in the BaseRequestHandler.
        """
        self.server.log.debug('Starting request hendler...')

        header_data = _RRN_TCP_HeaderData_v3()
        header_data.from_binary(self.request.recv(SIZE_RRN_TCP_HEADERDATA_V3))

        if (not header_data.is_right_struct() or
                header_data.data_type != RRNDATA_COMMANDS or
                header_data.data_length != SIZE_RRCOMMANDS):

            self.server.continueLoop = False
            self.server.log.error("TCP header is wrong!")
            self.server.log.info("ID: %s != %s" % (header_data.structure_id, STRUCTURE_ID_RRN_TCP_HEADER_DATA_V3))
            self.server.log.info("ID: %s != %s" % (header_data.data_type, RRNDATA_COMMANDS))
            self.server.log.info("ID: %s != %s" % (header_data.data_length, SIZE_RRCOMMANDS))
            return

        command = _RRCommands()
        command.from_binary(self.request.recv(SIZE_RRCOMMANDS))

        if not command.is_right_struct():
            self.server.continueLoop = False
            self.error.info("ID: %s != %s" % (command.structure_id, STRUCTURE_ID_RRCOMMANDS))
            return

        if command.param_slength == 0:
            self.server.log.error('Empty command received!')
            return

        self.server.next_command = command.param_s


class rrKSOServer(SocketServer.TCPServer):

    # TODO(Kirill): Ask Holger about asynchronous behaviour.
    # SocketServer.ThreadingMixIn
    # The mix-in classes override process_request() to start a
    # new thread or process when a request is ready to be handled,
    # and the work is done in the new child.

    def __init__(self, server_address, request_handler):
        self.daemon_threads = True
        self.request_handler = request_handler
        self.allow_reuse_address = True
        self.continue_loop = True
        self.next_command = '' # Set by rrKSOTCPHandler
        self.log = Logger()
        SocketServer.TCPServer.__init__(self, server_address, request_handler)

    def handle_timeout(self):
        self.log.error('Timeout!')
        self.continue_loop = False

    def handle_error(self, request, client_address):
        self.log.error('Issue while handline connection to %s:%s' % client_address)
        self.continue_loop = False
        self.log.error(traceback.format_exc())

    def handle_command(self):
        """
        Wait for a request from client then try to execute it.
        """
        while self.continue_loop:
            try:
                self.log.info('RR TCP waiting for new command...')
                self.handle_request()

            except Exception, e:
                self.log.error(e)
                self.continue_loop = False;
                self.log.info(traceback.format_exc())

            self.log.info('Next command is %s' % self.next_command)
            if len(self.next_command) > 0:
                if (self.next_command == 'ksoQuit()' or
                        self.next_command == 'ksoQuit()\n'):
                    self.continue_loop = False
                    self.next_command = ''
                else:
                    self.log.info('Executing command "%s"' % self.next_command)
                    exec (self.next_command)
                    next_command = ''

        self.log.info('RR TCP connection closed')

def create_placeholder(file_name, frame_number=None, padding=None, ext=None):

    if frame_number is not None:
        if padding is None:
            padding = 4
        file_name = filename + frame_number.zfill(padding) + ext

    host_name = socket.gethostname()[:100]
    with open(file_name, "wb") as f:
        f.write("rrDB") # Magic ID
        f.write("\x01\x0B") # DataType ID
        for x in range(0, len(host_name)):
            f.write(host_name[x])
            f.write("\x00") # Unicode
        for x in range(len(host_name),51):
            f.write("\x00\x00")
        f.write(chr(len(host_name)))
        f.write("\x00")
        f.write("\x00\x00")

if __name__ == '__main___':
    HOST, PORT = "localhost", 7774
    server = rrKSOServer((HOST, PORT), rrKSOTCPHandler)
    server.handle_command()
