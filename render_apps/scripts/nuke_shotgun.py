
import nuke
import os
import sys
import platform
import random
import string

# TODO(Kirill): Need to find a way for users to specify this path in not hardcoded way
sys.path.append('/Volumes/EARTH/SGProjectConfig/install/core/python')
import sgtk

def write_info(msg):
    print msg

def start_nuke_engime(work_area_path):
    """
    Initilize Shotgun Toolkit from the given context
    path and start the engine. For more info check:
    https://support.shotgunsoftware.com/entries/95440797#Render%20Farm%20Integration%201
    returns: Nuke SGTK Instance
    """
    tk = sgtk.sgtk_from_path(work_area_path)
    tk.synchronize_filesystem_structure()
    ctx = tk.context_from_path(work_area_path)
    # Attempt to start the engine for this context
    engine = sgtk.platform.start_engine('tk-nuke', tk, ctx)
    write_info('Shotgun Toolkit Nuke engine was initilized.')
    return engine

def convert_sg_write_nodes(sg_engine):
    """
    Convert all Shotgun write nodes found in the current Script to regular
    Nuke Write nodes.  Additional toolkit information will be stored on
    additional user knobs named 'tk_*'
    """
    app = sg_engine.apps["tk-nuke-writenode"]
    for n in app.get_write_nodes():
        write_info('Found "%s" shotgun write node.' % n.name())
    write_info('Converting to nuke write nodes...')
    # For function implementation check:
    # https://github.com/shotgunsoftware/tk-nuke-writenode/blob/master/python/tk_nuke_writenode/handler.py
    app.convert_to_write_nodes()
    write_info('All Shotgun write nodes was converted.')

def make_local_scene(pyModPath, orgFilename, locFilename,
                     orgDir, orgDirWinDrive, locDir):
    """
    Process and save new nuke file for future render.
    """

    # TODO(Kirill): This need to be replaced with path to global SG Toolkit
    # config e.g [SG]/install/core/python
    if (len(pyModPath) > 0):
        sys.path.append(pyModPath)

    # Start SG Nuke engine and conver all SG write node to Nuke Write
    engine = start_nuke_engime(orgFilename)
    nuke.scriptOpen(orgFilename)

    sg_write_nodes = nuke.allNodes(group=nuke.root(),
                                    filter='WriteTank',
                                    recurseGroups = True)
    # Store SG write nodes output paths
    sg_write_paths = {}
    for n in sg_write_nodes:
        sg_write_paths[n.name()] = n.knob('tk_cached_proxy_path').value()

    convert_sg_write_nodes(engine)

    # Set original output path to all newly converted write nodes
    nuke_write_nodes = nuke.allNodes('Write')
    for n in nuke_write_nodes:
        n.knob('file').setValue(sg_write_paths[n.name()])

    write_info('Render output path: %s' % n.knob('file').value())

    write_info('Saving nuke script to %s' % locFilename)
    nuke.scriptSaveAs(locFilename, 1)

    write_info('')
    write_info('Local scene created successufuly')
    write_info('')

if (len(sys.argv) > 5):
    make_local_scene(sys.argv[1], sys.argv[2], sys.argv[3],
                       sys.argv[4], sys.argv[5], sys.argv[6])
else:
    make_local_scene(sys.argv[1], sys.argv[2], sys.argv[3], "", "", "")
