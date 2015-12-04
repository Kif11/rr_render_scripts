import  rrGlobal
import  rrSG
import  rr

def updateStatsCmd():
    print "Update render stats in shotgun"
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-sgid")
    parser.add_argument("-avMemUsage")
    parser.add_argument("-avRenderTime")
    args = parser.parse_args()
    if ((len(args.sgid)<=1) or (args.sgid=="none")):
        print("Job has no Shotgun ID.")
        return
    
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()

    renderEntity= rRifle._findRenderEntity(args.sgid)
    renderEntity['average_render_time']=args.avRenderTime
    memFloat=float(args.avMemUsage)
    renderEntity['average_memory_usage']=memFloat
    rRifle._updateRenderEntity(args.sgid,renderEntity)
  
updateStatsCmd()
