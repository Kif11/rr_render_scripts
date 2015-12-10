import sys
import time
import datetime

class Logger(object):

	def __init__ (self, debug=False):

		self._INFO = 'INFO'
		self._WARNING = 'WARNING'
		self._ERROR = 'ERROR'
		self._DEBUG = 'DEBUG'
		self._SEP_CHAR = '-'

		self.debug_active = debug

	def make_msg(self, msg, msg_type = ''):
		cur_time = datetime.datetime.now().strftime('%H:%M:%S')
		new_msg = '%s %s: %s' %(cur_time, msg_type, msg)

		return new_msg

	def log(self, msg):
		print msg
		self.flush();

	def info(self, msg):
		msg = self.make_msg(msg, self._INFO)
		self.log(msg)

	def warning(self, msg):
		msg = self.make_msg(msg, self._WARNING)
		self.log(msg)

	def debug(self, msg):
		if (self.debug_active):
			msg = self.make_msg(msg, self._DEBUG)
			self.log(msg)
		else:
			pass

	def error(self, msg):
		msg = self.make_msg(msg, self._ERROR)
		self.log(msg)

		# raise NameError('Error reported, aborting render script!')

	def line(self):
		"""
		Print separation line on 80 char length to
		improve log readability.
		"""
		self.log(self._SEP_CHAR * 80)

	def flush(self):
		sys.stdout.flush()
		sys.stderr.flush()
