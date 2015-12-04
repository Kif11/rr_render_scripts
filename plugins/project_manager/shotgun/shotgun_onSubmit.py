import  rrGlobal
import  rrSG
import  rr

def submitRender():
    rrGlobal.progress_SetMaxA(3)
    rrGlobal.progress_SetProgressA(0)
    rrGlobal.refreshUI()
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()
    rrGlobal.progress_SetProgressA(1)
    rrGlobal.refreshUI()


    jobFirst= rr.jobSelected_get(0)
    submitUser=jobFirst.userName
    projectName=jobFirst.companyProjectName
    sequenceId=jobFirst.customSeqName
    shotId=jobFirst.customShotName
    renderDataList = []
    for jNr in range(0, rr.jobSelected_count()):
        job= rr.jobSelected_get(jNr)
        renderDataAdd = {'job_id':job.IDstr(), 'render_pass':job.layer, 'render_camera':job.camera, 'render_application':job.renderer.name, 'render_scene_name':job.sceneName}
        renderDataList.append(renderDataAdd)

    #create new submit and render entity
    submitEntity=rRifle.submitRender(renderDataList, submitUser, projectName, sequenceId, shotId, taskId=None)
    print("submitEntity is " +submitEntity)
    rrGlobal.progress_SetProgressA(2)
    for jNr in range(0, rr.jobSelected_count()):
        job= rr.jobSelected_get(jNr)
        shreID= rRifle.getRenderEntityFromRRJobId(job.IDstr())
        print("RenderEntity is " +shreID)
        rr.jobAll_setShotgunID(jNr,shreID)
        rr.jobSelected_set(jNr,job)
    rrGlobal.progress_SetProgressA(3)

submitRender()
