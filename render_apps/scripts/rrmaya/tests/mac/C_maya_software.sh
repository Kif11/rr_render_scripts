#!/bin/csh -f

"/Applications/Autodesk/maya2015/Maya.app/Contents/bin/maya" -batch -command '     source "/Users/amy/rrServer/render_apps/scripts/kso_maya.mel"; rrStartWrapper("/Users/amy/rrServer/render_apps/scripts", " PyModPath: /Users/amy/rrServer/render_apps/scripts, Renderer: mayaSoftware, SName: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/scenes/rr_mayasoftaware_01.ma, Db: /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/, KSOMode: false, Camera: persp, FDir:  /Users/amy/rrServer/render_apps/scripts/rrmaya/tests/projects/mayasoftware/images , FNameNoVar: test_01.  , FName: test_01  , FPadding: 4, FExt: .png,   FrStart: 2, FrEnd: 3, FrStep: 1 , FrOffset: 0 , Threads:  4,       ") '