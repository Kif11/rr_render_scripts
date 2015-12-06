#!/bin/csh -f
renice +15 -p $$
/bin/echo  '++++++++++++++++++++++++ Log Start +++++++++++++++++++++++++' 
/bin/echo  'Amys-MacBook-Pro  rrClient console     7.0.26    rrVer7.0.26      DEMO' 
/bin/echo  '11.23 14:13.15' 
/bin/echo  'Client is running on OSX 10.10.5 x64 4(HT)x2.5 Intel 6.5Ghz' 
/bin/echo  'Job: {0QR}  Sequence: 1-10, 9' 
/bin/echo  'Scene: .../    vray/    rr_vray_01 120.33Kb 11.23 14:12.20' 
/bin/echo  'Render config used: Maya vray   3D02__Maya2009__Vray.cfg' 
/bin/echo  'Executable used: /Applications/Autodesk/maya2015/Maya.app/Contents/bin/Render   ' 
setenv rrExeBit "x64"
/bin/echo 'rrExeBit x64'
setenv rrExeVersion "2015.0"
/bin/echo 'rrExeVersion 2015.0'
setenv rrExeVersionMinReq "2015"
/bin/echo 'rrExeVersionMinReq 2015'
setenv rrExeVersionMajor "2015"
/bin/echo 'rrExeVersionMajor 2015'
setenv rrExeVersionMinor "0"
/bin/echo 'rrExeVersionMinor 0'
setenv rrExeOS "mac"
/bin/echo 'rrExeOS mac'
/bin/echo  '++++++++++++ Environment Variables Job: ++++++++++++++++++++' 
setenv rrJobRenderapp "Maya"
/bin/echo 'rrJobRenderapp Maya'
setenv rrJobRenderer "vray"
/bin/echo 'rrJobRenderer vray'
setenv rrJobRendererVersion "3.10.01"
/bin/echo 'rrJobRendererVersion 3.10.01'
setenv rrJobProject "rrServer"
/bin/echo 'rrJobProject rrServer'
setenv rrJobType "3D"
/bin/echo 'rrJobType 3D'
setenv rrJobBit "x64"
/bin/echo 'rrJobBit x64'
setenv rrJobVersion "2015.16"
/bin/echo 'rrJobVersion 2015.16'
setenv rrJobVersionMajor "2015"
/bin/echo 'rrJobVersionMajor 2015'
setenv rrJobVersionMinor "16"
/bin/echo 'rrJobVersionMinor 16'
setenv rrJobTiled "false"
/bin/echo 'rrJobTiled false'
setenv rrJobCustomScene ""
/bin/echo 'rrJobCustomScene '
setenv rrJobCustomShot ""
/bin/echo 'rrJobCustomShot '
setenv rrJobCustomVersion "ray"
/bin/echo 'rrJobCustomVersion ray'
setenv rrJobSceneOS "mac"
/bin/echo 'rrJobSceneOS mac'
/bin/echo  '++++++++++++ Environment Variables Client: +++++++++++++++++' 
setenv rrClientName "Amys-MacBook-Pro"
/bin/echo 'rrClientName Amys-MacBook-Pro'
setenv rrClientCores "4"
/bin/echo 'rrClientCores 4'
setenv rrClientCoresUsed "4"
/bin/echo 'rrClientCoresUsed 4'
setenv rrClientBit "x64"
/bin/echo 'rrClientBit x64'
setenv rrClientRenderInstance "0"
/bin/echo 'rrClientRenderInstance 0'
setenv rrClientThreadID "0"
/bin/echo 'rrClientThreadID 0'
setenv rrClientThreadIDstr "A"
/bin/echo 'rrClientThreadIDstr A'
setenv RR_ROOT "/Users/amy/rrServer"
/bin/echo 'RR_ROOT /Users/amy/rrServer'
setenv rrBin "/Users/amy/rrServer/bin/mac/"
/bin/echo 'rrBin /Users/amy/rrServer/bin/mac/'
setenv rrPlugins "/Users/amy/rrServer/render_apps/renderer_plugins/maya/mac_x64/"
/bin/echo 'rrPlugins /Users/amy/rrServer/render_apps/renderer_plugins/maya/mac_x64/'
setenv rrPluginsNoOS "/Users/amy/rrServer/render_apps/renderer_plugins/maya/"
/bin/echo 'rrPluginsNoOS /Users/amy/rrServer/render_apps/renderer_plugins/maya/'
setenv rrPrefs "/Users/amy/rrServer/render_apps/renderer_prefs/maya/mac_x64/"
/bin/echo 'rrPrefs /Users/amy/rrServer/render_apps/renderer_prefs/maya/mac_x64/'
setenv rrSharedExeDir "/Users/amy/rrServer/render_apps/renderer_exe/maya/mac_x64/"
/bin/echo 'rrSharedExeDir /Users/amy/rrServer/render_apps/renderer_exe/maya/mac_x64/'
setenv rrLocalTemp "/Users/Shared/RR_localdata/temp/A/"
/bin/echo 'rrLocalTemp /Users/Shared/RR_localdata/temp/A/'
setenv TEMP "/Users/Shared/RR_localdata/temp/A"
/bin/echo 'TEMP /Users/Shared/RR_localdata/temp/A'
setenv TMP "/Users/Shared/RR_localdata/temp/A"
/bin/echo 'TMP /Users/Shared/RR_localdata/temp/A'
setenv rrLocalRoot "/Users/Shared/RR_localdata/"
/bin/echo 'rrLocalRoot /Users/Shared/RR_localdata/'
setenv rrLocalExeDir "/Users/Shared/RR_localdata/renderer_exe/maya/mac_x64/"
/bin/echo 'rrLocalExeDir /Users/Shared/RR_localdata/renderer_exe/maya/mac_x64/'
setenv rrLocalPrefs "/Users/Shared/RR_localdata/renderer_prefs/maya/mac_x64/"
/bin/echo 'rrLocalPrefs /Users/Shared/RR_localdata/renderer_prefs/maya/mac_x64/'
setenv rrLocalPlugins "/Users/Shared/RR_localdata/renderer_plugins/maya/mac_x64/"
/bin/echo 'rrLocalPlugins /Users/Shared/RR_localdata/renderer_plugins/maya/mac_x64/'
setenv rrBaseAppPath "/Applications/Autodesk/maya2015/Maya.app/Contents"
/bin/echo 'rrBaseAppPath /Applications/Autodesk/maya2015/Maya.app/Contents'
/bin/echo  '++++++++++++ Environment Variables Done  +++++++++++++++++++' 
 
 
/bin/echo  'source \"/Users/Shared/RR_localdata/_global.sh\"' 
source "/Users/Shared/RR_localdata/_global.sh" 
/bin/echo  'source \"/Users/Shared/RR_localdata/maya.sh\"' 
source "/Users/Shared/RR_localdata/maya.sh" 
/bin/echo  '\"/Users/amy/rrServer/bin/mac64/rrResetexitcode\"' 
"/Users/amy/rrServer/bin/mac64/rrResetexitcode" 
/bin/echo  '\"/Applications/Autodesk/maya2015/Maya.app/Contents/bin/maya\" -batch -command      source \"/Users/amy/rrServer/render_apps/scripts/kso_maya.mel\"; rrStartWrapper(\"/Users/amy/rrServer/render_apps/scripts\", \" PyModPath: /Users/amy/rrServer/render_apps/scripts, Renderer: vray, SName: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/scenes/rr_vray_01.ma, Db: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/,  Camera: persp, FDir:  /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/images , FNameNoVar: rr_vray_01.  , FName: rr_vray_01  , FPadding: 4, FExt: .png,   FrStart: 1, FrEnd: 10, FrStep: 9 , FrOffset: 0 , Threads:  4,       \") ' 
"/Applications/Autodesk/maya2015/Maya.app/Contents/bin/maya" -batch -command '     source "/Users/amy/rrServer/render_apps/scripts/kso_maya.mel"; rrStartWrapper("/Users/amy/rrServer/render_apps/scripts", " PyModPath: /Users/amy/rrServer/render_apps/scripts, Renderer: vray, SName: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/scenes/rr_vray_01.ma, Db: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/,  Camera: persp, FDir:  /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/vray/images , FNameNoVar: rr_vray_01.  , FName: rr_vray_01  , FPadding: 4, FExt: .png,   FrStart: 1, FrEnd: 10, FrStep: 9 , FrOffset: 0 , Threads:  4,       ") ' 
"/Users/amy/rrServer/bin/mac64/rrCheckexitcode" $? 0 0 1 
/bin/echo  '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' 
/bin/echo  'Amys-MacBook-Pro  rrClient console     7.0.26    rrVer7.0.26      DEMO' 
/bin/echo  'Job ID: {0QR}' 
/bin/echo  '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' 


