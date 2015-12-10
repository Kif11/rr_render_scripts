import os
import sys
import datetime
import time
import pymel.core as pm
import maya.mel
parent_dir = os.path.join(os.getcwd(), '..')
sys.path.append(parent_dir)
import rrapp.application
reload(rrapp.application)
from rrapp.application import RRApp
from utils.hook import Hook
import utils.argparser
reload(utils.argparser)
from utils.argparser import ArgumentParser
import rrtcp
from utils.logger import Logger

# TODO(Kirill) Add render region back for all renders.
# We need it for multi tile render.

class RRMayaJob(object):

    def __init__(self, args_string):
        self.arg = ArgumentParser('RRMaya', args_string)
        self.log = Logger()
        self.workspace = self.arg.get('Database')
        self.image_dir = self.arg.get('FDir')
        self.python_path = self.arg.get('PyModPath')
        self.maya_scene = self.arg.get('SName')
        self.override_render_cmd = self.arg.get('OverwriteRenderCmd')
        self.kso_mode = self.arg.get('KSOMode')
        self.file_name = self.arg.get('FName')
        self.file_ext = self.arg.get('FExt')
        self.file_name_no_var = self.arg.get('FNameNoVar')
        self.file_dir = self.arg.get('FDir')
        self.single_output = self.arg.get('FSingleOutput')
        self.frame_padding = self.arg.default('FPadding', 4)
        self.frame_start = self.arg.get('FrStart')
        self.frame_end = self.arg.get('FrEnd')
        self.frame_step = self.arg.get('FrStep')
        self.frame_offset = self.arg.get('FrOffset')
        self.camera = self.arg.get('Camera')
        self.layer_name = self.arg.get('Layer')
        self.threads = self.arg.get('Threads')
        self.resx = self.arg.get('ResX')
        self.resy = self.arg.get('ResY')
        self.image_format = self.arg.get('FOverrideFormat')
        self.threads = self.arg.get('Threads')
        self.edge_aa = self.arg.get('AA1')
        self.samples = self.arg.get('AA2')
        self.max_samples = self.arg.get('AA3')
        self.treshold = self.arg.get('AA4')
        self.rx1 = self.arg.get('RegionX1')
        self.rx2 = self.arg.get('RegionX2')
        self.ry1 = self.arg.get('RegionY1')
        self.ry2 = self.arg.get('RegionY2')
        self.motion_blur = self.arg.get('RenderMotionBlur')
        self.render_demo = self.arg.get('RenderDemo')
        self.render_displace = self.arg.get('RenderDisplace')
        self.ext_override = self.arg.get('FExtOverride')
        self.verbose = self.arg.get('Verbose')
        self.kso_mode = self.arg.get('KSOMode')

    @property
    def render_name(self):
        """
        returns: Name of the current renderer provided
        by rrSubmiter or specified in Maya settings.
        """
        render_globals = pm.PyNode('defaultRenderGlobals')
        render_name = self.arg.get('Renderer')

        if (render_name is None):
            return render_globals.getAttr('currentRenderer')
        else:
            return render_name

    @property
    def render_layer(self):
        """
        Setup the Maya renderer to render only the specified layers.
        In case when arg layer is None will set masterLayer as rendarable.
        param layer: Layer name string.
        """
        user_layer = self.arg.get('Layer')
        lm = pm.PyNode('renderLayerManager')
        render_layers = lm.listConnections()

        rendarable_layer = None
        for l in render_layers:
            if l.name() == user_layer:
                l.setAttr('renderable', True)
                rendarable_layer = l.name()
            else:
                l.setAttr('renderable', False)
        if rendarable_layer is None:
            # This is the case when render specified by user does not exist or None.
            default_layer = pm.nodetypes.RenderLayer(u'defaultRenderLayer')
            default_layer.setAttr('renderable', True)
            self.log.warning('Failed to set layer %s as renderable. ' \
                             'Does not exists. Set to %s.' \
                             % (user_layer, default_layer.name()))
            rendarable_layer = default_layer.name()

        self.log.info('Current render layer: %s' % rendarable_layer)

        return rendarable_layer

class RRMaya(RRApp):

    def __init__(self, rr_job):
        super(self.__class__, self).__init__()
        self.job = rr_job
        self.hook = Hook(self)
        self.GLOABAL_STARTUP_PLUGINS = ['xgenMR', 'xgenToolkit', 'AbcImport']
        self.WORK_SPACE = {
            'images': self.job.image_dir,
            'depth': self.job.image_dir
        }

    def version(self):
        """
        returns: Maya app version e.g 2015.
        """
        # Return full api version as 201516
        # We trim two last digits to produce 2015
        version = cmds.about(apiVersion=True)/100
        self.log.info("Maya version: %s" % version)
        return version

    def open_scene(self, scene):
        """
        Open maya scene.
        param scene: Path to maya scene file.
        """
        scene = pm.openFile(scene, force=True)
        self.log.info('Open scene file: %s' % scene)
        return scene

    def set_workspace(self):
        # workspace.open doesn't do anything if workspace.open = None
        pm.workspace.open(self.job.workspace)
        self.log.info('Maya workspace: %s' % pm.workspace.getcwd())
        for file_rule, path in self.WORK_SPACE.items():
            pm.workspace.fileRules[file_rule] = path

    def load_plugin(self, plugin_name):
        # Maya will skip this action if plugin is alredy loaded
        maya.mel.eval('loadPlugin %s;' % plugin_name)

    def override_attr(self, attr, value):
        """
        Overide attribute value.
        param attr: PyMel atribute object.
        param value: New value for the attribute.
        """
        # Removes any render layer adjustment
    	# and unlocks the attr,
    	# so that command line rendering can override the value.
        maya.mel.eval('removeRenderLayerAdjustmentAndUnlock %s;' % attr.name())
        attr.set(value)

        return attr

    def set_attrs(self, node, attr_dict):
        """
        param node: PyMel note to assign attributes to.
        param attr_dict: Dictionlary of Attribute name : value.
        """
        for name, value in attr_dict.items():
            if (value is not None):
                node.setAttr(name, value)
            else:
                # self.log.debug('Attribute %s is %s. Skipped!' % (name, value))
                pass

    def set_default_render_resolution(self, x, y):
        """
        Set resolution for all native Maya renders.
        param x: Resolution X
        param y: Resolution Y
        """
        default_res = pm.PyNode('defaultResolution')
        if (x is not None):
            default_res.setAttr('width', x)
            self.log.info('Render width: %s' % x)
        if (y is not None):
            default_res.setAttr('height', y)
            self.log.info('Render height: %s' % y)

    def init_mayasoftware(self):

        render_globals = pm.PyNode('defaultRenderGlobals')
        render_quality = pm.PyNode('defaultRenderQuality')

        self.set_default_render_resolution(self.job.resx, self.job.resy)
        if self.job.image_format is not None:
            pm.mel.setMayaSoftwareImageFormat(self.job.image_format)

        self.set_attrs(render_globals, {
            'numCpusToUse': self.job.threads,
            'motionBlur': self.job.motion_blur
        })

        self.set_attrs(render_quality, {
             'edgeAntiAliasing': self.job.edge_aa,
             'shadingSamples': self.job.samples,
             'maxShadingSamples': self.job.max_samples,
             'redThreshold': self.job.treshold,
             'greenThreshold': self.job.treshold,
             'blueThreshold': self.job.treshold,
             'coverageThreshold': self.job.treshold
        })

        # Set render rigion. Need for multi-tiled rendering.
        region = (self.job.rx1, self.job.rx2, self.job.ry1, self.job.ry2)
        if not None in region:
            pm.mel.setMayaSoftwareRegion(*region)

    def init_mentalray(self):

        mi_default = pm.PyNode('miDefaultOptions')

        self.load_plugin('Mayatomr')
        # This function call from mentalrayUI.mel required
        # to initialize render properly.
        pm.mel.miCreateDefaultNodes()

        self.set_default_render_resolution(self.job.resx, self.job.resy)
        if self.job.image_format is not None:
            pm.mel.setMentalRayImageFormat(self.job.image_format)

        # Set global mental ray variables.
        for name, value in {
            'VerbosityOn': 'true',
            'Verbosity': self.job.verbose,
            'NumThreadOn': 'true',
            'NumThread': self.job.threads,
            'NumThreadAutoOn': 'true',
            'NumThreadAuto': 'true'}.items():
            if (value is not None):
                cmd = 'global int $g_mrBatchRenderCmdOption_%s = %s;' % (name, value)
                maya.mel.eval(cmd)

        self.set_attrs(mi_default, {
            'displacementShaders': self.job.render_displace,
            'miDefaultOptions': self.job.edge_aa,
            'maxSamples': self.job.samples,
            'contrastR': self.job.max_samples,
            'contrastG': self.job.max_samples,
            'contrastB': self.job.max_samples,
            'contrastA': self.job.max_samples,
            'motionBlur': self.job.motion_blur
        })

    def init_vray(self):

        vray_settings = pm.PyNode('vraySettings')

        self.load_plugin('vrayformaya')
        # pm.mel.loadPreferredRenderGlobalsPreset('vray') # Not sure that we need it.
        pm.mel.vrayRegisterRenderer()
        pm.mel.vrayCreateVRaySettingsNode()

        self.set_attrs(vray_settings, {
            'animation': True,
            'fileNamePrefix': self.job.file_name,
            'sys_max_threads': self.job.threads,
            'width': self.job.resx,
            'height': self.job.resy,
            'fileNamePadding': self.job.frame_padding,
            'batchCamera': self.job.camera,
            'imageFormatStr': self.job.image_format
        })

    def init_arnold(self):

        self.load_plugin('mtoa')

        ai_render = pm.PyNode('defaultArnoldRenderOptions')
        ai_driver = pm.PyNode('defaultArnoldDriver')
        ai_translator = ai_driver.ai_translator

        ext_dict = {'.exr': 'exr', '.jpeg': 'jpeg', '.jpg': 'jpeg',
                    '.maya': 'maya', '.png': 'png', '.tif': 'tif'}

        self.set_attrs(ai_render, {
            'renderType': 0,
            'threads_autodetect': False,
            'threads': self.job.threads,
            'motion_blur_enable': self.job.motion_blur,
            'ignoreMotionBlur': not self.job.motion_blur,
            'ignoreDisplacement': not self.job.render_displace,
            'abortOnLicenseFail': not self.job.render_demo,
            'skipLicenseCheck': self.job.render_demo,
            'log_verbosity': self.job.verbose
        })

        if (self.job.image_format is not None):
            ai_translator.set(self.job.image_format)
        if (self.job.ext_override is not None):
            new_ext = ext_dict[self.job.file_ext.lower()]
            ai_translator.set(new_ext)

    def init_redshift(self):
        pass

    def render_frame(self, frame_number):
        """
        Render one frame.
        """
        render_globals = pm.PyNode('defaultRenderGlobals')

        before_frame = datetime.datetime.now()

        self.set_attrs(render_globals, {
            'startFrame': frame_number,
            'endFrame': frame_number,
            'startExtension': frame_number + self.job.frame_offset
        })

        self.log.info('Starting to render frame %s...' % frame_number)
        # global proc mayaBatchRenderProcedure(
        # 	int $isInteractiveBatch,	// interactive batch or command line rendering
        # 	string $sceneName,			// the original scene name before export
        # 	string $layer,				// render specific layer
        # 	string $renderer,			// use specific renderer is not empty string.
        # 	string $option				// optional arg to the render command
        # )
        # TODO(Kirill): Test with user custom render layers.
        pm.mel.mayaBatchRenderProcedure(0, "", self.job.render_layer, self.job.render_name, "")

        after_frame = datetime.datetime.now() - before_frame

        self.log.info("Randering of frame: %s finished in %s (h:m:s.ms)"
                                          % (frame_number, after_frame))

    def render_frames(self):

        render_globals = pm.PyNode('defaultRenderGlobals')
        renderer = self.job.render_name

        # Before starting render execute user script.
        self.hook.before_segment_render()

        self.log.info('Changing scene frame to frame %s...' % self.job.frame_start)

        render_globals.setAttr('byFrameStep', self.job.frame_step)
        render_globals.setAttr('byExtension', self.job.frame_step)

        pm.mel.setImageSizePercent(-1.)
        render_globals.setAttr('renderAll', 1)

        frange = (self.job.frame_start,
                  self.job.frame_end + 1,
                  self.job.frame_step)

        for frame in xrange(*frange):
            self.hook.before_frame_render()
            file_name = '%s/%s' % (self.job.file_dir, self.job.file_name_no_var)
            rrtcp.create_placeholder(file_name,
                                     frame,
                                     self.job.frame_padding,
                                     self.job.file_ext)

            self.render_frame(frame)
        # Run user code after render of segment is finished
        self.hook.after_segment_render()

    def initialize(self):

        default_res = pm.PyNode('defaultResolution')
        render_globals = pm.PyNode('defaultRenderGlobals')

        self.set_env('PYTHONPATH', self.job.python_path)

        for p in self.GLOABAL_STARTUP_PLUGINS:
            self.load_plugin(p)

        self.set_workspace()
        self.open_scene(self.job.maya_scene)
        # self.set_render_layer(self.job.render_layer)

        self.log.line()
        self.log.info('Start render initilization.')
        self.log.line()

        renderer = self.job.render_name
        if (renderer == 'mayaSoftware'):
            self.init_mayasoftware()
        elif (renderer == 'mentalRay'):
            self.init_mentalray()
        elif (renderer == 'vray'):
            self.init_vray()
        elif (renderer == 'arnold'):
            self.init_arnold()
        elif (renderer == 'redshift'):
            self.init_redshift()

        self.log.line()
        self.log.info('Render init finished.')
        self.log.line()

        if (self.job.kso_mode):
            self.start_kso_server()
        else:
            self.render_frames()


def rr_start(args_string):
    rr_job = RRMayaJob(args_string)
    rr_maya = RRMaya(rr_job)
    rr_maya.initialize()
