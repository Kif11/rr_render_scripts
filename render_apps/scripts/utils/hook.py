from logger import Logger
# import maya.cmds as cmds

class Hook(object):

	def __init__(self, parent):
		"""
		This class contains set of functions that
		called from RRMaya, RR3dsmax etc. Users can
		write their custom code as well as access
		parrent class variables and methods trough
		self.parent variable.
		:param parent: Parent class from which this
		hook had been called.
		"""
		self.log = Logger()

		# Contain instance of the parent
		# class from which it was called
		# e.g RRMaya, RR3dsMax, etc.
		self.parent = parent

	def before_segment_render(self):
		self.log.info('Running before segment render hook...')

	def after_segment_render(self):
		self.log.info('Running after segment render hook...')

	def before_frame_render(self):
		self.log.info('Running before frame render hook...')
