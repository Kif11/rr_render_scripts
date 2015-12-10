#  Render script for Maya
#  Last Change: v 7.0.20
#  Copyright (c)  Holger Schoenberger - Binary Alchemy

import datetime
import time
import sys
import re
import os
import maya.cmds as cmds
import pymel.core as pm
import maya.mel

parent_dir = os.path.join(os.getcwd(), '..')
sys.path.append(parent_dir)

from rrapp import Application
from utils.hook import Hook
import rrtcp


class RRMaya(Application):

    def __init__ (self, args_string):
        super(self.__class__, self).__init__(args_string)
        self.log.debug('Initilizing RRMaya...')

        self.rend = MayaRenderer(self)

        # Command argument values
        self.workspace = self.arg.get('Database')
        self.image_dir = self.arg.get('FDir')
        self.python_path = self.arg.get('PyModPath')
        self.maya_scene = self.arg.get('SName')
        self.layer_name = self.arg.get('Layer')
        self.override_render_cmd = self.arg.get('OverwriteRenderCmd')
        self.kso_mode = self.arg.get('KSOMode')

        self.log.debug('Initilization of RRMaya finished')

    def app_version(self):
        # Return full api version as 201516
        # We trim two last digits to produce 2015
        version = cmds.about(apiVersion=True)/100
        self.log.info("Maya version: %s" % version)
        return version

    def open_scene(self, scene):
        scene = cmds.file(scene, f=True, o=True)
        self.log.info('Open scene file: %s' % scene)
        return scene

    def init_globals(self):

        self.set_env('PYTHONPATH', self.python_path)

        if (self.workspace is not None):
            cmds.workspace(self.workspace, openWorkspace=True )
            self.log.info("Maya workspace: %s" % self.workspace)
        if (self.image_dir is not None):
            cmds.workspace(fileRule = ["images", self.image_dir])
            cmds.workspace(fileRule = ["depth", self.image_dir])
            self.log.info("Maya image directory: %s" % self.image_dir)

        # Load global plugins
        maya.mel.eval("loadPlugin AbcImport;")
        if (self.app_version() >= 2014):
            maya.mel.eval("loadPlugin xgenMR;")
            maya.mel.eval("loadPlugin xgenToolkit;")

        self.open_scene(self.maya_scene)
        self.set_render_layer(self.layer_name)

    def set_render_layer(self, layer_name):

        # TODO(Kirill): Refactor this function using PyMel

        if (layer_name is not None):

            self.log.info('Current layer: %s' % layer_name)

            if (layer_name == 'masterLayer'):
                layer_name = 'defaultRenderLayer'

            render_layers = cmds.listConnections('renderLayerManager',
                                                 t='renderLayer')

            if (not layer_name.upper() in (name.upper() for name in render_layers)):
                self.log.error('Layer "%s" does not exist!' % layer_name)

            maya.mel.eval('setMayaSoftwareLayers("%s");' % layer_name)

    def start_render(self):

        time_start = datetime.datetime.now()

        # Maya and render initialization
        self.init_globals()
        self.rend.initialize()

        time_end = datetime.datetime.now() - time_start

        self.log.info("Scene load time: %s (h:m:s.ms)" % time_end)
        self.log.info("Scene initialization finished. Starting to render...")

        if (self.kso_mode):
            self.start_kso_server()
        else:
            self.rend.render_frames()

        self.log.info('Render finished.')


class MayaRenderer(object):

    def __init__(self, rrmaya):
        """
        :rrmaya object: Parent RRMaya object
        """
        self.log = rrmaya.log
        self.log.debug('Initilizing MayaRenderer...')

        self.rrmaya = rrmaya
        self.arg = rrmaya.arg

        self.hook = Hook(self)

        self.render_globals = pm.PyNode('defaultRenderGlobals')

        # Command argument values
        self.renderer = self.get_renderer()
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
        self.format = self.arg.get('FOverrideFormat')
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

        self.init_globals()

        self.log.debug('Initilization of MayaRenderer finished')

    def init_globals(self):
        """
        This function is global for all renders. It run on the
        class instantiation.
        """

        def unlock_default_global(param):
            maya.mel.eval('removeRenderLayerAdjustmentAndUnlock '
                          'defaultRenderGlobals.%s;' % param)

        default_res = pm.PyNode('defaultResolution')

        if (self.single_output is None):
            unlock_default_global('animation')
            # self.render_globals.setAttr('imageFilePrefix', self.file_name )
            self.render_globals.setAttr('animation', True)

            unlock_default_global('endFrame')
            unlock_default_global('byFrameStep')
            unlock_default_global('modifyExtension')
            unlock_default_global('startExtension')

            self.render_globals.setAttr('modifyExtension', 1)
            self.render_globals.setAttr('extensionPadding', self.frame_padding)

        if (self.camera is not None):
            maya.mel.eval('makeCameraRenderable("%s")' % self.camera)
            self.log.info('Camera: %s' % self.camera)

        if (self.threads is not None):
            cmds.threadCount(n=self.threads)
            self.log.info('Threads: %s' % self.threads)

        # Set default render resolution
        if (self.resx is not None):
            default_res.setAttr('width', self.resx)
            self.log.info('Render width: %s' % self.resx)
        if (self.resy is not None):
            default_res.setAttr('height', self.resy)
            self.log.info('Render height: %s' % self.resy)

        self.render_globals.setAttr('skipExistingFrames', 0)
        maya.mel.eval('setImageSizePercent(-1.)')
        self.render_globals.setAttr('renderAll', 1)

    def get_renderer(self):
        render_name = self.arg.get('Renderer')
        # If no renderer argument specified
        # retrive renderer from maya settings
        if (render_name is None):
            maya_renderer = self.render_globals.getAttr('currentRenderer')
            render_name = self.arg.set('Renderer', maya_renderer)

        self.log.info('Maya renderer: %s' % render_name)

        return render_name

    def initialize(self):

        if (self.renderer == "mayaSoftware"):
            self.init_mayasoftware()
        elif (self.renderer == "mentalRay"):
            self.init_mentalray()
        elif (self.renderer == "vray"):
            self.init_vray()
        elif (self.renderer == "arnold"):
            self.init_arnold()
        elif (self.renderer == "redshift"):
            self.init_redshift()

    def init_mayasoftware(self):

        self.log.debug("INITILAZING MAYA SOFTWARE")

        quality = pm.PyNode('defaultRenderQuality')

        if (self.format is not None):
            maya.mel.eval('setMayaSoftwareImageFormat("%s")' % self.format)

        globals_attrs = {'numCpusToUse': self.threads,
                         'motionBlur': self.motion_blur}

        for name, value in globals_attrs.items():
            if (value is not None):
                self.render_globals.setAttr(name, value)

        quality_attrs = {
             'edgeAntiAliasing': self.edge_aa,
             'shadingSamples': self.samples,
             'maxShadingSamples': self.max_samples,
             'redThreshold': self.treshold,
             'greenThreshold': self.treshold,
             'blueThreshold': self.treshold,
             'coverageThreshold': self.treshold}

        for name, value in quality_attrs.items():
            if (value is not None):
                render_quality.setAttr(name, value)


    def init_mentalray(self):

        self.log.debug("INITILAZING MENTAL RAY SOFTWARE")

        maya.mel.eval('loadPlugin Mayatomr;')
        maya.mel.eval('miLoadMayatomr;')
        maya.mel.eval('miCreateDefaultNodes();')

        mi_default = pm.PyNode('miDefaultOptions')

        # TODO(Kirill): May be I can replace this long maya mell commands
        # with PyMel commands
        if (self.format is not None):
            maya.mel.eval('setMentalRayImageFormat("%s")' % self.format)
        if (self.verbose is not None):
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_VerbosityOn = true;'
                          'global int $g_mrBatchRenderCmdOption_Verbosity = %s' % self.verbose)

        if (self.threads is not None):
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_NumThreadOn = true;'
                          'global int $g_mrBatchRenderCmdOption_NumThread = %s' % self.threads)
        else:
            maya.mel.eval('global int $g_mrBatchRenderCmdOption_NumThreadAutoOn = true;'
                          'global int $g_mrBatchRenderCmdOption_NumThreadAuto = true')

        maya.mel.eval('setMentalRayRenderRegion(%s,%s,%s,%s)'
                                              % (self.rx1, self.rx2,
                                                 self.ry1, self.ry2))

        if (self.motion_blur is not None):
            if (self.motion_blur):
                mi_default.setAttr('motionBlur', 2)
            else:
                mi_default.setAttr('motionBlur', 0)

        mi_attrs = {'displacementShaders': self.render_displace,
                    'miDefaultOptions': self.edge_aa,
                    'maxSamples': self.samples,
                    'contrastR': self.max_samples,
                    'contrastG': self.max_samples,
                    'contrastB': self.max_samples,
                    'contrastA': self.max_samples}

        for name, value in mi_attrs.items():
            if (value is not None):
                mi_default.setAttr(name, value)

    def init_vray(self):
        vr_render = pm.PyNode('vraySettings')

        vr_render.setAttr('animation', True)
        vr_render.setAttr('fileNamePrefix', self.file_name)
        maya.mel.eval('vrayRegisterRenderer(); vrayCreateVRaySettingsNode();')
        if (self.threads is not None):
            vr_render.setAttr('sys_max_threads', self.threads)

        # TODO(Kirill): This setting cause very long render time
        # Tested on maya 2016 with vray 3. Do we realy need it?
        # # Set vray render region
        # maya.mel.eval('vraySetBatchDoRegion(%s,%s,%s,%s)'
        # 				% (self.rx1, self.rx2, self.ry1, self.ry2))

        vray_attrs = {'width': self.resx,
                      'height': self.resy,
                      'fileNamePadding': self.frame_padding,
                      'batchCamera': self.camera,
                      'imageFormatStr': self.format}

        for name, value in vray_attrs.items():
            if (value is not None):
                vr_render.setAttr(name, value)
                self.log.debug('Vray attr %s set to %s'
                				% (name, value))

    def init_arnold(self):

        ai_render = pm.PyNode('defaultArnoldRenderOptions')
        ai_driver = pm.PyNode('defaultArnoldDriver')
        ai_translator = ai_driver.ai_translator

        ai_render.setAttr('renderType', 0)

        if (self.single_output is None and
                self.file_name is not None):
            self.file_name = self.file_name.replace('<Layer>', '<RenderLayer>')
            self.file_name = self.file_name.replace('<layer>', '<RenderLayer>')
            self.render_globals.setAttr('imageFilePrefix', self.file_name)

        if (self.threads is not None):
            ai_render.setAttr('threads_autodetect', False)
            ai_render.setAttr('threads', self.threads)

        if (self.motion_blur is not None):
            ai_render.setAttr('motion_blur_enable', self.motion_blur)
            ai_render.setAttr('ignoreMotionBlur', not self.motion_blur)

        if (self.render_demo is not None):
            if (self.render_demo):
                ai_render.setAttr('abortOnLicenseFail', False)
                ai_render.setAttr('skipLicenseCheck', True)
            else:
                ai_render.setAttr('abortOnLicenseFail', True)
                ai_render.setAttr('skipLicenseCheck', False)

        if (self.render_displace is not None):
            ai_render.setAttr('ignoreDisplacement', not self.render_displace)

        if (self.format is not None):
            ai_translator.set(self.format)

        if (self.ext_override is not None):
            ext_dict = {'.exr': 'exr', '.jpeg': 'jpeg', '.jpg': 'jpeg',
                        '.maya': 'maya', '.png': 'png', '.tif': 'tif'}
            ai_translator.set(ext_dict[self.file_ext.lower()])

        # Set render region
        regions = {'regionMinX': self.rx1, 'regionMaxX': self.rx2,
                   'regionMinY': self.ry1, 'regionMaxY': self.ry2}

        for name, value in regions.items():
            if value is not None:
                ai_render.setAttr(name, value)

        if (self.verbose is not None):
            ai_render.setAttr('log_verbosity', self.verbose)

    def init_redshift(self):
        pass

    def render_frame(self, frame_number):

        before_frame = datetime.datetime.now()

        self.log.info('Starting to render frame %s...' % frame_number)

        self.render_globals.setAttr('startFrame', frame_number)
        self.render_globals.setAttr('endFrame', frame_number)
        self.render_globals.setAttr('startExtension', frame_number +
                                                self.frame_offset)

        # Render one frame
        maya.mel.eval('mayaBatchRenderProcedure(0, "", "%s", "%s", "")'
                                    % (self.layer_name, self.renderer))

        after_frame = datetime.datetime.now() - before_frame

        self.log.info("Randering of frame: %s finished in %s (h:m:s.ms)"
                                          % (frame_number, after_frame))

    def render_frames(self):

        # Before starting render execute user script
        self.hook.before_segment_render()

        self.log.info('Changing scene frame to frame %s...' % self.frame_start)
        cmds.currentTime(self.frame_start, edit=True)

        self.render_globals.setAttr('byFrameStep', self.frame_step)
        self.render_globals.setAttr('byExtension', self.frame_step)

        if (self.renderer == 'vray'):
            setAttr('vraySettings.startFrame', self.frame_start)
            setAttr('vraySettings.endFrame', self.frame_end)
            setAttr('vraySettings.frameStep', self.frame_step)

        maya.mel.eval('setImageSizePercent(-1.)')
        self.render_globals.setAttr('renderAll', 1)

        frame_range = xrange(self.frame_start, self.frame_end + 1, self.frame_step)

        for frame in frame_range:
            self.hook.before_frame_render()
            file_name = '%s/%s.' % (self.file_dir, self.file_name_no_var)
            rrtcp.create_placeholder(file_name, frame, self.frame_padding, self.file_ext)

            self.render_frame(frame)

        # Run user code after render of segment is finished
        self.hook.after_segment_render()

        # if (argValid(arg.FNameNoVar)):
        #     if (Renderer == "vray" and not arg.FNameNoVar.endswith('.')):
        #         kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar+".", frameNr, arg.FPadding, arg.FExt)
        #     else:
        #         kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar, frameNr, arg.FPadding, arg.FExt)

def rrStart(args_string):
    rr_maya = RRMaya(args_string)
    rr_maya.start_render()
