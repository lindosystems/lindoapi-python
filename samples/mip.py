#  Solve an MIP model.
#
#  The problem:
#
#      Minimize x1 + x2 + x3 + x4 + x5 + x6
#      s.t.
#               [r1]x1 + x2 + x3 + x4 + x5 + x6  >=3
#               [r2]x1 + x2                      <=1
#               [r3]     x2 + x3                 <=1
#               [r4]               x4 + x5 + x6  <=2
#               [r5]               x4 +      x6  <=1
#
#               x1,x2,x3,x4,x5,x6 are binary variables

import lindo
import numpy as np
import os
import sys
def logFunc(pModel,line, udict): 
    # use end="" to stop print from adding an extra
    # newline to the line string
    print(f"{line}", end="")

def cbFunc(pModel,iloc, udict): 
    dObj = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,iloc,lindo.LS_DINFO_CUR_OBJ,dObj)
    dIter = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,iloc,lindo.LS_DINFO_CUR_ITER,dIter)    
    print(f"\ncbFunc| LOC:{iloc} Iter:{dIter[0]}, Obj={dObj[0]}",end =" ")
  

def cbMIPFunc(pModel,udict,dObj,padPrimal):     
    dIter = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,0,lindo.LS_DINFO_CUR_ITER,dIter)    
    print(f"\ncbMIPFunc| Iter:{dIter[0]}, Obj={dObj}",end =" ")
    for k,x in enumerate(padPrimal): 
        tempVar = str(udict["varType"][k])[2:-1] # use [2:-1] to replace b'B' with B 
        print(f"\n{padPrimal[k]:.5f} {tempVar}",end=" ")


#model data
nCons = 5
nVars = 6
nDir = 1
dObjConst = 0.0
adC = np.array([1.,1.,1.,1.,1.,1.],dtype=np.double)
adB = np.array([3.0,1.0,1.0,2.0,1.0],dtype=np.double)
acConTypes = np.array(['G','L','L','L','L'],dtype='|S1')
nNZ = 15
anBegCol = np.array([0,2,5,7,10,12,15],dtype=np.int32)
pnLenCol = np.asarray(None)
adA = np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],dtype=np.double)
anRowX = np.array([0,1,0,1,2,0,2,0,3,4,0,3,0,3,4],dtype=np.int32)
pdLower = np.array([0,0,0,0,0,0],dtype=np.double)
pdUpper = np.array([1.,1.,1.,1.,1.,1.],dtype=np.double)
pachVarType = np.array(['B','B','B','B','B','B'],dtype='|S1')


# The first try block is for catching errors rasied while creating an environment
try:
    #create LINDO environment
    LicenseKey = np.array('',dtype='S1024')
    lindo.pyLSloadLicenseString(os.getenv('LINDOAPI_HOME')+'/license/lndapi160.lic',LicenseKey)
    pnErrorCode = np.array([-1],dtype=np.int32)
    pEnv = lindo.pyLScreateEnv(pnErrorCode,LicenseKey)
except lindo.LINDO_Exception as e:
    print(e.args[0])
    exit(1)

try:
    pModel = lindo.pyLScreateModel(pEnv,pnErrorCode)



    #load data into the model
    print("Loading LP data..")
    lindo.pyLSloadLPData(pModel,nCons,nVars,nDir,
                        dObjConst,adC,adB,acConTypes,nNZ,anBegCol,
                        pnLenCol,adA,anRowX,pdLower,pdUpper)
    # Set variable types after the LPData is loaded
    verstr = lindo.getversion(pEnv)
    lindo.pyLSloadVarType(pModel,pachVarType)
    # Set up the callback functions
    udict = {
    "prefix": "APILOG",
    "postfix": "..",
    "version": verstr,
    "varType": pachVarType,
    }

    lindo.pyLSsetModelLogfunc(pModel,logFunc, udict)
    lindo.pyLSsetMIPCallback(pModel,cbMIPFunc, udict)
    
    #solve the model
    print("Solving the model..")
    pnStatus = np.array([-1],dtype=np.int32)
    lindo.pyLSsolveMIP(pModel,pnStatus)

    #retrieve the objective value
    dObj = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetInfo(pModel,lindo.LS_DINFO_MIP_OBJ,dObj)
    print(f"Objective is: {dObj[0]:.5f}")
    print("")

    #retrieve the primal solution
    varType = np.empty((nVars),dtype=np.byte)
    lindo.pyLSgetVarType(pModel,varType)

    padPrimal = np.empty((nVars),dtype=np.double)
    lindo.pyLSgetMIPPrimalSolution(pModel,padPrimal)
    print("Primal solution is: ")
    for k,x in enumerate(padPrimal): 
        tmpVarType = chr(varType[k])
        print(f"{padPrimal[k]:.5f} {tmpVarType}")
        
    #delete LINDO model pointer
    lindo.pyLSdeleteModel(pModel)
    #delete LINDO environment pointer
    lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")