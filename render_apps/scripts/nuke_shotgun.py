
import nuke
import os
import sys
import platform
import random
import string

# Command line arguments
sgtk_path = sys.argv[1]
original_nuke_file = sys.argv[2]
local_nuke_file = sys.argv[3]

# Append SG Tank path to PYTHONPATH
sys.path.append(sgtk_path)

import sgtk

# TODO(Kirill):
# We need to use global submission script instead of this local one.
# Nuke local submission script path: /Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/plugins/rrSubmit_Nuke_5.py
#
# Config path: /Users/amy/rrServer/render_apps/_config/C13__Nuke5_shotgun.cfg

# TODO(Kirill): I need to unify this script with the main nuke_local localrenderout
# and make it pretty!

# TODO(Kirill): Replace with the Logger module.
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

def make_local_scene(original_nuke_file, local_nuke_file):
    """
    Open Nuke file in its original location; conver all SG Write nodes to
    normal Nuke node; save the file to temp local directore.

    param original_nuke_file: Path to original Nuke file. Should be valid
    SG Toolkit project.
    param local_nuke_file: Path to temp nuke file. Provided by the rrServer.
    """

    # Start SG Nuke engine and conver all SG write node to Nuke Write
    engine = start_nuke_engime(original_nuke_file)
    nuke.scriptOpen(original_nuke_file)

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

    write_info('Saving nuke script to %s' % local_nuke_file)
    nuke.scriptSaveAs(local_nuke_file, 1)

    write_info('')
    write_info('Local scene created successufuly')
    write_info('')

if __name__ == '__main__':
    make_local_scene(original_nuke_file, local_nuke_file)
