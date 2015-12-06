import os, sys
parent_dir = os.path.join(os.getcwd(), '..')
sys.path.append(parent_dir)
from utils.logger import Logger
from utils.argparser import ArgumentParser
from rrtcp import rrKSOServer, rrKSOTCPHandler

class RRApp(object):
    """
    Abstract base class for all rr job renderer aplications.
    """
    def __init__(self):
        self.log = Logger(debug=True)

    def version(self):
        raise NotImplementedError()

    def open_scene(self):
        raise NotImplementedError()

    def set_env(self, name, value):
        if (value is not None):
            os.environ[name] = value
            self.log.info('Environmental variable "%s" set to "%s"'
                                                    % (name, value))
        else:
            self.log.info('Can not set environment "%s" to "%s"'
                                                    % (name, value))

    def start_kso_server(self):
        """
        This function perform Keep Scene Open RR functionality.
        Start TCP server and listen for commands from client.
        """
        KSO_HOST = "localhost"
        KSO_PORT = 7774
        server = rrKSOServer((KSO_HOST, KSO_PORT), rrKSOTCPHandler)
        server.handle_command()

    def start_render(self):
        raise NotImplementedError()
