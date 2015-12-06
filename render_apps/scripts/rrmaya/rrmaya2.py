import os
import sys
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

class RRMayaJob(object):
    def __init__(self, args_string):
        arg = ArgumentParser('RRMaya', args_string)
        self.render_name = arg.get('Renderer')
        self.workspace = arg.get('Database')
        self.image_dir = arg.get('FDir')
        self.python_path = arg.get('PyModPath')
        self.maya_scene = arg.get('SName')
        self.render_layer = arg.get('Layer')
        self.override_render_cmd = arg.get('OverwriteRenderCmd')
        self.kso_mode = arg.get('KSOMode')
        self.file_name = arg.get('FName')
        self.file_ext = arg.get('FExt')
        self.file_name_no_var = arg.get('FNameNoVar')
        self.file_dir = arg.get('FDir')
        self.single_output = arg.get('FSingleOutput')
        self.frame_padding = arg.default('FPadding', 4)
        self.frame_start = arg.get('FrStart')
        self.frame_end = arg.get('FrEnd')
        self.frame_step = arg.get('FrStep')
        self.frame_offset = arg.get('FrOffset')
        self.camera = arg.get('Camera')
        self.layer_name = arg.get('Layer')
        self.threads = arg.get('Threads')
        self.resx = arg.get('ResX')
        self.resy = arg.get('ResY')
        self.image_format = arg.get('FOverrideFormat')
        self.threads = arg.get('Threads')
        self.edge_aa = arg.get('AA1')
        self.samples = arg.get('AA2')
        self.max_samples = arg.get('AA3')
        self.treshold = arg.get('AA4')
        self.rx1 = arg.get('RegionX1')
        self.rx2 = arg.get('RegionX2')
        self.ry1 = arg.get('RegionY1')
        self.ry2 = arg.get('RegionY2')
        self.motion_blur = arg.get('RenderMotionBlur')
        self.render_demo = arg.get('RenderDemo')
        self.render_displace = arg.get('RenderDisplace')
        self.ext_override = arg.get('FExtOverride')
        self.verbose = arg.get('Verbose')
        self.kso_mode = arg.get('KSOMode')

class RRMaya(RRApp):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.job = RRMayaJob(" PyModPath: /Users/amy/rrServer/render_apps/scripts, Renderer: mayaSoftware, SName: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/scenes/rr_mayasoftaware_01.ma, Db: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/, KSOMode: true, Camera: persp, FOverrideFormat: png, FDir:  /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/images , FNameNoVar: test_01.  , FName: test_01  , FPadding: 4, FExt: .png,   FrStart: 2, FrEnd: 3, FrStep: 1 , FrOffset: 0 , Threads:  4,       ")
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
        scene = pm.openFile(scene)
        self.log.info('Open scene file: %s' % scene)
        return scene

    def set_workspace(self):
        # workspace.open doesn't do anything if workspace.open = None
        pm.workspace.open(self.job.workspace)
        self.log.info('Maya workspace: %s' % pm.workspace.getcwd())
        for file_rule, path in self.WORK_SPACE.items():
            pm.workspace.fileRules[file_rule] = path

    @property
    def render_name(self):
        """
        returns: Name of the current renderer provided
        by rrSubmiter or specified in Maya settings.
        """
        if (self.job.render_name is None):
            return self.render_globals.getAttr('currentRenderer')
        else:
            return self.job.render_name

    def load_plugin(self, plugin_name):
        # Maya will skip this action if plugin is alredy loaded
        maya.mel.eval('loadPlugin %s;' % plugin_name)

    def set_render_layer(self, layer):
        """
        Setup the Maya renderer to render only the specified layers.
        In case when arg layer is None will set masterLayer as rendarable.
        param layer: Layer name string.
        """
        lm = pm.PyNode('renderLayerManager')
        render_layers = lm.listConnections()

        selected = False
        for l in render_layers:
            if l.name() == layer:
                l.setAttr('renderable', True)
                selected = True
            else:
                l.setAttr('renderable', False)
        if not selected:
            # This is the case when render specified by user does not exist or None.
            default_layer = pm.nodetypes.RenderLayer(u'defaultRenderLayer')
            default_layer.setAttr('renderable', True)
            self.log.warning('Failed to set layer %s as renderable. ' \
                             'Does not exists. Set to master layer.' % layer)
        else:
            self.log.info('Current render layer: %s' % layer)

        # Old approach
        # maya.mel.eval('setMayaSoftwareLayers("%s", "%s");' % (layer, passes))

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
                self.log.debug('Attribute %s is %s. Skipped!' % (name, value))

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

        # TODO(kirill): Start refactoring this.

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

    def initialize(self):

        default_res = pm.PyNode('defaultResolution')
        render_globals = pm.PyNode('defaultRenderGlobals')

        self.set_env('PYTHONPATH', self.job.python_path)

        for p in self.GLOABAL_STARTUP_PLUGINS:
            self.load_plugin(p)

        self.set_workspace()
        self.open_scene(self.job.maya_scene)
        self.set_render_layer(self.job.render_layer)

        renderer = self.render_name
        if (renderer == "mayaSoftware"):
            self.init_mayasoftware()
        elif (renderer == "mentalRay"):
            self.init_mentalray()
        elif (renderer == "vray"):
            self.init_vray()
        elif (renderer == "arnold"):
            self.init_arnold()
        elif (renderer == "redshift"):
            self.init_redshift()

        if (self.job.kso_mode):
            self.start_kso_server()
        else:
            self.render()

if __name__ == '__main__':
    pass
