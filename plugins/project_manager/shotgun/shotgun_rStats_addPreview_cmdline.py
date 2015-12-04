import  rrGlobal
import  rrSG
import  rr

def addPreviewCmd():
    print "Adding preview images to shotgun"
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-sgid")
    parser.add_argument("-p1")
    parser.add_argument("-p2")
    parser.add_argument("-p3")
    args = parser.parse_args()
    shreID=args.sgid
    if ((len(shreID)<=1) or (shreID=="none")):
        print("Job has no Shotgun ID.")
        return
    
    import royalRifle
    global rRifle
    rRifle=royalRifle.RoyalRifle()

    pathList = []
    pathList.append(args.p1)
    pathList.append(args.p2)
    pathList.append(args.p3)
    rRifle.addPreviewImages(shreID, pathList)
  

addPreviewCmd()
