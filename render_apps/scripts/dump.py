def logSetAttr(setParam,setValue):
    logMessageGen("SET",str(setParam)+" = "+str(setValue))
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")
        

def setAttr(setParam,setValue):
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")
        

def logSetAttrType(setParam,setValue,setType):
    logMessageGen("SET",str(setParam)+" = "+str(setValue))
    if cmds.objExists(setParam):
        maya.mel.eval("removeRenderLayerAdjustmentAndUnlock "+str(setParam)+";")
        cmds.setAttr(setParam,setValue, type=setType)
    else:
        logMessageGen("WRN","Unable to set value. "+str(setParam)+" does not exist!")


def renderFrames(arg, FrStart, FrEnd, FrStep, FrOffset, Renderer, Layer):
    try:
        if (not argValid(arg.FPadding)):
            arg.FPadding = 4
        arg.FPadding = int(arg.FPadding)
        FrStart=int(FrStart)
        FrStart=int(FrStart)
        FrEnd=int(FrEnd)
        FrStep=int(FrStep)
        logMessage("Changing scene frame to frame #"+str(FrStart)+" ...")
        cmds.currentTime( FrStart, edit=True )    
        setAttr("defaultRenderGlobals.byFrameStep",FrStep)
        setAttr("defaultRenderGlobals.byExtension",int(FrStep))    
        if (Renderer == "vray"):
            setAttr("vraySettings.frameStep",FrStep)
        maya.mel.eval("setImageSizePercent(-1.)")
        setAttr("defaultRenderGlobals.renderAll",1)
        

        for frameNr in xrange(FrStart,FrEnd+1,FrStep):
            logMessage("Starting to render frame #"+str(frameNr)+" ...")
            if (argValid(arg.FNameNoVar)):
                if (Renderer == "vray" and not arg.FNameNoVar.endswith(".")):
                    kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar+".", frameNr, arg.FPadding, arg.FExt)
                else:
                    kso_tcp.writeRenderPlaceholder_nr(arg.FDir+"/"+arg.FNameNoVar, frameNr, arg.FPadding, arg.FExt)
            beforeFrame=datetime.datetime.now()

            # TODO(Kirill): Execute before frame client"s script 

            setAttr("defaultRenderGlobals.startFrame",frameNr)
            setAttr("defaultRenderGlobals.endFrame",frameNr)
            setAttr("defaultRenderGlobals.startExtension",int(frameNr)+int(FrOffset))
            if (Renderer == "vray"):
                setAttr("vraySettings.startFrame",frameNr)
                setAttr("vraySettings.endFrame",frameNr)
            flushLog()

            # Render a frame
            maya.mel.eval("mayaBatchRenderProcedure(0, "", "" + str(Layer) + "", "" + str(Renderer) + "", "")")
            

            flushLog()
            afterFrame=datetime.datetime.now()
            afterFrame=afterFrame-beforeFrame

            # TODO(Kirill): Execute after frame client"s script 

            logMessage("Frame #"+str(frameNr)+" done. Frame Time: "+str(afterFrame)+"  h:m:s.ms")
            flushLog()
        
    except Exception as e:
        logMessageError(str(e))

    



def ksoRenderFrame(FrStart,FrEnd,FrStep ):
  global globalArg
  renderFrames(globalArg,FrStart,FrEnd,FrStep, globalArg.FrOffset, globalArg.Renderer, globalArg.Layer)
  flushLog()
  logMessage("rrKSO Frame(s) done #"+str(FrEnd)+" ")
  logMessage("                                                            ")
  logMessage("                                                            ")
  logMessage("                                                            ")
  flushLog()




def rrKSOStartServer(arg):
  try:
      logMessage("rrKSO startup...")
      if ((arg.KSOPort== None) or (len(str(arg.KSOPort))<=0)):
          arg.KSOPort=7774
      HOST, PORT = "localhost", int(arg.KSOPort)
      server = kso_tcp.rrKSOServer((HOST, PORT), kso_tcp.rrKSOTCPHandler)
      flushLog()
      time.sleep(0.3)
      logMessage("rrKSO server started")
      flushLog()
      kso_tcp.rrKSONextCommand=""
      while server.continueLoop:
          try:
              logMessageDebug("rrKSO waiting for new command...")
              server.handle_request()
              time.sleep(1) # handle_request() seem to return before handle() completed execution
          except Exception, e:
              logMessageError(e)
              server.continueLoop= False;
              import traceback
              logMessageError(traceback.format_exc())
          logMessage("rrKSONextCommand ""+ kso_tcp.rrKSONextCommand+""")   
          logMessage("                                                         ...")
          logMessage("                                                          . ")
          logMessage("                                                         ...")
          flushLog()
          if (len(kso_tcp.rrKSONextCommand)>0):
              if ((kso_tcp.rrKSONextCommand=="ksoQuit()") or (kso_tcp.rrKSONextCommand=="ksoQuit()\n")):
                  server.continueLoop=False
                  kso_tcp.rrKSONextCommand=""
              else:
                  exec (kso_tcp.rrKSONextCommand)
                  kso_tcp.rrKSONextCommand=""
      logMessage("rrKSO closed")
  except Exception as e:
      logMessageError(str(e))


def render_KSO(arg):
  rrKSOStartServer(arg)


def render_default(arg):
  renderFrames (arg, arg.FrStart, arg.FrEnd, arg.FrStep, arg.FrOffset, arg.Renderer, arg.Layer)


def render_overwrite(arg):
  cmdline=arg.OverwriteRenderCmd
  cmdline=cmdline.replace("aFrStart",str(arg.FrStart))
  cmdline=cmdline.replace("aFrEnd",str(arg.FrEnd))
  cmdline=cmdline.replace("aFrStep",str(arg.FrStep))
  if (argValid(arg.FDir)):
      cmdline=cmdline.replace("aFDir",str(arg.FDir))
  if (argValid(arg.FName)):
      cmdline=cmdline.replace("aFName","""+str(arg.FName)+""")
  if (argValid(arg.ArchiveExportName)):
      cmdline=cmdline.replace("aArchiveExportName","""+str(arg.ArchiveExportName)+""")
  if (argValid(arg.FrOffset)):
      cmdline=cmdline.replace("aFrOffset",str(arg.FrOffset))
  if (argValid(arg.Renderer)):
      cmdline=cmdline.replace("aRenderer",str(arg.Renderer))
  if (argValid(arg.Layer)):
      cmdline=cmdline.replace("aLayer",str(arg.Layer))
  if (argValid(arg.Camera)):
      cmdline=cmdline.replace("aCamera",str(arg.Camera))
  logMessage("Executing custom mel line "+cmdline)
  ret=maya.mel.eval(cmdline)
  print ret



def setRenderSettings_MayaSoftware(arg):
  try:
      logSetAttr("defaultRenderGlobals.skipExistingFrames",0)
      if (argValid(arg.FOverrideFormat)): 
          maya.mel.eval("setMayaSoftwareImageFormat(""+arg.FOverrideFormat+"")")
      if (argValid(arg.Threads)):
          logSetAttr("defaultRenderGlobals.numCpusToUse",int(arg.Threads))
      if (argValid(arg.AA1)): 
          logSetAttr("defaultRenderQuality.edgeAntiAliasing",int(arg.AA1))
      if (argValid(arg.AA2)): 
          logSetAttr("defaultRenderQuality.shadingSamples",int(arg.AA2))
      if (argValid(arg.AA3)): 
          logSetAttr("defaultRenderQuality.maxShadingSamples",int(arg.AA3))
      if (argValid(arg.AA4)): 
          logSetAttr("defaultRenderQuality.redThreshold",float(arg.AA4))
          logSetAttr("defaultRenderQuality.greenThreshold",float(arg.AA4))
          logSetAttr("defaultRenderQuality.blueThreshold",float(arg.AA4))
          logSetAttr("defaultRenderQuality.coverageThreshold",float(arg.AA4))
      if (argValid(arg.RegionX1)):
          if (not argValid(arg.RegionX2)):    
              arg.RegionX2=19999
          if (not argValid(arg.RegionY1)):    
              arg.RegionY1=0
          if (not argValid(arg.RegionY2)):    
              arg.RegionY2=19999
          maya.mel.eval("setMayaSoftwareRegion("+str(arg.RegionX1)+","+str(arg.RegionX2)+","+str(arg.RegionY1)+","+str(arg.RegionY2)+")")
      if (argValid(arg.RenderMotionBlur)): 
          logSetAttr("defaultRenderGlobals.motionBlur",arg.RenderMotionBlur)
  except Exception as e:
      logMessageError(str(e))        


def setRenderSettings_MRay(arg):
  try:
      logSetAttr("defaultRenderGlobals.skipExistingFrames",0)
      if (argValid(arg.FOverrideFormat)): 
          maya.mel.eval("setMentalRayImageFormat(""+arg.FOverrideFormat+"")")
      if (argValid(arg.Verbose)):
          maya.mel.eval("global int $g_mrBatchRenderCmdOption_VerbosityOn = true; global int $g_mrBatchRenderCmdOption_Verbosity = "+str(arg.Verbose))
      if (argValid(arg.Threads)):
          maya.mel.eval("global int $g_mrBatchRenderCmdOption_NumThreadOn = true; global int $g_mrBatchRenderCmdOption_NumThread = "+str(arg.Threads))
      else:
          maya.mel.eval("global int $g_mrBatchRenderCmdOption_NumThreadAutoOn = true; global int $g_mrBatchRenderCmdOption_NumThreadAuto = true")
      if (argValid(arg.RegionX1)):
          if (not argValid(arg.RegionX2)):    
              arg.RegionX2=19999
          if (not argValid(arg.RegionY1)):    
              arg.RegionY1=0
          if (not argValid(arg.RegionY2)):    
              arg.RegionY2=19999
          maya.mel.eval("setMentalRayRenderRegion("+str(arg.RegionX1)+","+str(arg.RegionX2)+","+str(arg.RegionY1)+","+str(arg.RegionY2)+")")
      if (argValid(arg.RenderDisplace)): 
          logSetAttr("miDefaultOptions.displacementShaders",arg.RenderDisplace)        
      if (argValid(arg.RenderMotionBlur)):
          if (arg.RenderMotionBlur):
              logSetAttr("miDefaultOptions.motionBlur",2)
          else:
              logSetAttr("miDefaultOptions.motionBlur",0)        
      if (argValid(arg.AA1)): 
          logSetAttr("miDefaultOptions.minSamples",int(arg.AA1))
      if (argValid(arg.AA2)): 
          logSetAttr("miDefaultOptions.maxSamples",int(arg.AA2))
      if (argValid(arg.AA3)): 
          logSetAttr("miDefaultOptions.contrastR",float(arg.AA3))
          logSetAttr("miDefaultOptions.contrastR",float(arg.AA3))
          logSetAttr("miDefaultOptions.contrastR",float(arg.AA3))
          logSetAttr("miDefaultOptions.contrastR",float(arg.AA3))
  except Exception as e:
      logMessageError(str(e))

    
def setRenderSettings_VRay(arg):
  try:
      logSetAttr("defaultRenderGlobals.skipExistingFrames",0)
      logSetAttr("vraySettings.animation",True)
      logSetAttrType("vraySettings.fileNamePrefix",arg.FName,"string")
      maya.mel.eval("vrayRegisterRenderer(); vrayCreateVRaySettingsNode();")
      if (argValid(arg.Threads)):
          logSetAttr("vraySettings.sys_max_threads",int(arg.Threads))
      if (argValid(arg.RegionX1)):
          if (not argValid(arg.RegionX2)):    
              arg.RegionX2=19999
          if (not argValid(arg.RegionY1)):    
              arg.RegionY1=0
          if (not argValid(arg.RegionY2)):    
              arg.RegionY2=19999
          maya.mel.eval("vraySetBatchDoRegion("+str(arg.RegionX1)+","+str(arg.RegionX2)+","+str(arg.RegionY1)+","+str(arg.RegionY2)+")")
      if (argValid(arg.ResX)): 
          logSetAttr("vraySettings.width",int(arg.ResX))
      if (argValid(arg.ResY)): 
          logSetAttr("vraySettings.height",int(arg.ResY))
      if (argValid(arg.FPadding)):
          logSetAttr("vraySettings.fileNamePadding",int(arg.FPadding))
      if (argValid(arg.Camera)):
          logSetAttrType("vraySettings.batchCamera",arg.Camera,"string")
      if (argValid(arg.FOverrideFormat)):
          logSetAttrType("vraySettings.imageFormatStr",arg.FOverrideFormat,"string")
  except Exception as e:
      logMessageError(str(e))        

def setRenderSettings_Arnold(arg):
  try:
      logSetAttr("defaultRenderGlobals.skipExistingFrames",0)
      logSetAttr("defaultArnoldRenderOptions.renderType",0)
      if (not argValid(arg.FSingleOutput)):
          arg.FName=arg.FName.replace("<Layer>","<RenderLayer>");
          arg.FName=arg.FName.replace("<layer>","<RenderLayer>");
          logSetAttrType("defaultRenderGlobals.imageFilePrefix",arg.FName,"string")
      if (argValid(arg.Threads)):
          logSetAttr("defaultArnoldRenderOptions.threads_autodetect",False)
          logSetAttr("defaultArnoldRenderOptions.threads",int(arg.Threads))
      if (argValid(arg.RenderMotionBlur)): 
          logSetAttr("defaultArnoldRenderOptions.motion_blur_enable",arg.RenderMotionBlur)
      if (argValid(arg.RenderDemo)):
          if (arg.RenderDemo):
              logSetAttr("defaultArnoldRenderOptions.abortOnLicenseFail",False)
              logSetAttr("defaultArnoldRenderOptions.skipLicenseCheck",True)
          else:
              logSetAttr("defaultArnoldRenderOptions.abortOnLicenseFail",True)
              logSetAttr("defaultArnoldRenderOptions.skipLicenseCheck",False)
      if (argValid(arg.RenderDisplace)): 
          logSetAttr("defaultArnoldRenderOptions.ignoreDisplacement",(not arg.RenderDisplace))        
      if (argValid(arg.RenderMotionBlur)):
          logSetAttr("defaultArnoldRenderOptions.ignoreMotionBlur",(not arg.RenderMotionBlur))
      if (argValid(arg.FOverrideFormat)):
          import pymel.core as pm
          dAD = pm.PyNode("defaultArnoldDriver")
          dAD.ai_translator.set(arg.FOverrideFormat)
      if (argValid(arg.FExtOverride)):
          import pymel.core as pm
          dAD = pm.PyNode("defaultArnoldDriver")
          arg.FExtOverride=arg.FExtOverride.lower()
          if (arg.FExtOverride==".exr"):
              dAD.ai_translator.set("exr")
          elif (arg.FExtOverride==".jpeg"):
              dAD.ai_translator.set("jpeg")
          elif (arg.FExtOverride==".jpg"):
              dAD.ai_translator.set("jpeg")
          elif (arg.FExtOverride==".maya"):
              dAD.ai_translator.set("maya")
          elif (arg.FExtOverride==".png"):
              dAD.ai_translator.set("png")
          elif (arg.FExtOverride==".tif"):
              dAD.ai_translator.set("tif")
      if (argValid(arg.RegionX1)):
          if (not argValid(arg.RegionX2)):    
              arg.RegionX2=19999
          if (not argValid(arg.RegionY1)):    
              arg.RegionY1=0
          if (not argValid(arg.RegionY2)):    
              arg.RegionY2=19999
          logSetAttr("defaultArnoldRenderOptions.regionMinX",int(arg.RegionX1))
          logSetAttr("defaultArnoldRenderOptions.regionMaxX",int(arg.RegionX2))
          logSetAttr("defaultArnoldRenderOptions.regionMinY",int(arg.RegionY1))
          logSetAttr("defaultArnoldRenderOptions.regionMaxY",int(arg.RegionY2))
      try:
          if (argValid(arg.Verbose)):
              logSetAttr("defaultArnoldRenderOptions.log_verbosity",int(arg.Verbose))
              logSetAttr("defaultArnoldRenderOptions.log_console_verbosity",int(arg.Verbose))
      except Exception as e:
          logMessageError(str(e))
  except Exception as e:
      logMessageError(str(e))   



def setRenderSettings_Redshift(arg):
  try:
      maya.mel.eval("redshiftRegisterRenderer(); redshiftGetRedshiftOptionsNode();")
      logSetAttrType("redshiftOptions.imageFilePrefix",arg.FName,"string")
      logSetAttr("redshiftOptions.skipExistingFrames",0)

      if (argValid(arg.CudaDevices)):
          arg.CudaDevices.replace(".",",")
          arg.CudaDevices="{"+arg.CudaDevices+"}"
          logMessageGen("SET"," CudaDevices = "+str(arg.CudaDevices))
          maya.mel.eval("redshiftSelectCudaDevices("+arg.CudaDevices+");")            
  except Exception as e:
      logMessageError(str(e))     