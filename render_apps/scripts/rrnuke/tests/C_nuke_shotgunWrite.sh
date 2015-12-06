#!/bin/csh -f
renice +15 -p $$
/bin/echo  '++++++++++++++++++++++++ Log Start +++++++++++++++++++++++++' 
/bin/echo  'Amys-MacBook-Pro  rrClient console     7.0.26    rrVer7.0.26      DEMO' 
/bin/echo  '11.25 14:30.12' 
/bin/echo  'Client is running on OSX 10.10.5 x64 4(HT)x2.5 Intel 6.5Ghz' 
/bin/echo  'Job: {M59a}  Sequence: 1-39, 1' 
/bin/echo  'Scene: .../    nuke/    scene.v001 2.78Kb 11.25 14:27.08' 
/bin/echo  'Render config used: Nuke shotgun   C13__Nuke5_shotgun.cfg' 
/bin/echo  'Executable used: /Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/Nuke9.0v6   ' 
setenv rrExeBit "x64"
/bin/echo 'rrExeBit x64'
setenv rrExeVersion "9.6"
/bin/echo 'rrExeVersion 9.6'
setenv rrExeVersionMinReq "9.6"
/bin/echo 'rrExeVersionMinReq 9.6'
setenv rrExeVersionMajor "9"
/bin/echo 'rrExeVersionMajor 9'
setenv rrExeVersionMinor "6"
/bin/echo 'rrExeVersionMinor 6'
setenv rrExeOS "mac"
/bin/echo 'rrExeOS mac'
/bin/echo  '++++++++++++ Environment Variables Job: ++++++++++++++++++++' 
setenv rrJobRenderapp "Nuke"
/bin/echo 'rrJobRenderapp Nuke'
setenv rrJobRenderer "shotgun"
/bin/echo 'rrJobRenderer shotgun'
setenv rrJobRendererVersion ""
/bin/echo 'rrJobRendererVersion '
setenv rrJobProject "pipeline_research_project"
/bin/echo 'rrJobProject pipeline_research_project'
setenv rrJobType "Comp"
/bin/echo 'rrJobType Comp'
setenv rrJobBit "x64"
/bin/echo 'rrJobBit x64'
setenv rrJobVersion "9.06"
/bin/echo 'rrJobVersion 9.06'
setenv rrJobVersionMajor "9"
/bin/echo 'rrJobVersionMajor 9'
setenv rrJobVersionMinor "06"
/bin/echo 'rrJobVersionMinor 06'
setenv rrJobTiled "false"
/bin/echo 'rrJobTiled false'
setenv rrJobCustomScene "cene"
/bin/echo 'rrJobCustomScene cene'
setenv rrJobCustomShot ""
/bin/echo 'rrJobCustomShot '
setenv rrJobCustomVersion ""
/bin/echo 'rrJobCustomVersion '
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
setenv rrPlugins "/Users/amy/rrServer/render_apps/renderer_plugins/nuke/mac_x64/"
/bin/echo 'rrPlugins /Users/amy/rrServer/render_apps/renderer_plugins/nuke/mac_x64/'
setenv rrPluginsNoOS "/Users/amy/rrServer/render_apps/renderer_plugins/nuke/"
/bin/echo 'rrPluginsNoOS /Users/amy/rrServer/render_apps/renderer_plugins/nuke/'
setenv rrPrefs "/Users/amy/rrServer/render_apps/renderer_prefs/nuke/mac_x64/"
/bin/echo 'rrPrefs /Users/amy/rrServer/render_apps/renderer_prefs/nuke/mac_x64/'
setenv rrSharedExeDir "/Users/amy/rrServer/render_apps/renderer_exe/nuke/mac_x64/"
/bin/echo 'rrSharedExeDir /Users/amy/rrServer/render_apps/renderer_exe/nuke/mac_x64/'
setenv rrLocalTemp "/Users/Shared/RR_localdata/temp/A/"
/bin/echo 'rrLocalTemp /Users/Shared/RR_localdata/temp/A/'
setenv TEMP "/Users/Shared/RR_localdata/temp/A"
/bin/echo 'TEMP /Users/Shared/RR_localdata/temp/A'
setenv TMP "/Users/Shared/RR_localdata/temp/A"
/bin/echo 'TMP /Users/Shared/RR_localdata/temp/A'
setenv rrLocalRoot "/Users/Shared/RR_localdata/"
/bin/echo 'rrLocalRoot /Users/Shared/RR_localdata/'
setenv rrLocalExeDir "/Users/Shared/RR_localdata/renderer_exe/nuke/mac_x64/"
/bin/echo 'rrLocalExeDir /Users/Shared/RR_localdata/renderer_exe/nuke/mac_x64/'
setenv rrLocalPrefs "/Users/Shared/RR_localdata/renderer_prefs/nuke/mac_x64/"
/bin/echo 'rrLocalPrefs /Users/Shared/RR_localdata/renderer_prefs/nuke/mac_x64/'
setenv rrLocalPlugins "/Users/Shared/RR_localdata/renderer_plugins/nuke/mac_x64/"
/bin/echo 'rrLocalPlugins /Users/Shared/RR_localdata/renderer_plugins/nuke/mac_x64/'
setenv rrBaseAppPath "/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS"
/bin/echo 'rrBaseAppPath /Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS'
/bin/echo  '++++++++++++ Environment Variables Done  +++++++++++++++++++' 
/bin/echo  'source \"/Users/Shared/RR_localdata/_global.sh\"' 
source "/Users/Shared/RR_localdata/_global.sh" 
/bin/echo  'source \"/Users/Shared/RR_localdata/nuke.sh\"' 
source "/Users/Shared/RR_localdata/nuke.sh" 
 
 
/bin/echo  ' \"/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/Nuke9.0v6\" -t \"/Users/amy/rrServer/render_apps/scripts/nuke_shotgun.py\" /Users/amy/rrServer/plugins/python_modules /Volumes/Collab/pipeline_research_project/sequences/SQ_A034/ADN_A034A/comp/work/nuke/scene.v001.nk /Users/Shared/RR_localdata/cachedscenes/Volumes_Collab/pipeline_research_project/59d4a248/nuke/scene.v001.nk  ' 
 "/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/Nuke9.0v6" -t "/Users/amy/rrServer/render_apps/scripts/nuke_shotgun.py" /Users/amy/rrServer/plugins/python_modules /Volumes/Collab/pipeline_research_project/sequences/SQ_A034/ADN_A034A/comp/work/nuke/scene.v001.nk /Users/Shared/RR_localdata/cachedscenes/Volumes_Collab/pipeline_research_project/59d4a248/nuke/scene.v001.nk   
/bin/echo  '\"/Users/amy/rrServer/bin/mac64/rrResetexitcode\"' 
"/Users/amy/rrServer/bin/mac64/rrResetexitcode" 
/bin/echo  '\"/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/Nuke9.0v6\" -X ShotgunWrite1  -f    -m 4 --priority low \"/Users/Shared/RR_localdata/cachedscenes/Volumes_Collab/pipeline_research_project/59d4a248/nuke/scene.v001.nk\" 1-39/1' 
"/Applications/Nuke9.0v6/Nuke9.0v6.app/Contents/MacOS/Nuke9.0v6" -X ShotgunWrite1  -f    -m 4 --priority low "/Users/Shared/RR_localdata/cachedscenes/Volumes_Collab/pipeline_research_project/59d4a248/nuke/scene.v001.nk" 1-39/1 
"/Users/amy/rrServer/bin/mac64/rrCheckexitcode" $? 0 0 1 
/bin/echo  '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' 
/bin/echo  'Amys-MacBook-Pro  rrClient console     7.0.26    rrVer7.0.26      DEMO' 
/bin/echo  'Job ID: {M59a}' 
/bin/echo  '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' 


