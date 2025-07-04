#  A Python programming example of interfacing with LINDO API.
#
#  The problem:
#
#      Minimize x1 + x2 + x3 + x4
#      s.t.
#              3x1              + 2x4   = 20
#                    6x2        + 9x4  >= 20
#              4x1 + 5x2 + 8x3          = 40
#                    7x2 + 1x3         >= 10
#
#               2 <= x1 <= 5
#               1 <= x2 <= +inf
#            -inf <= x3 <= 10
#            -inf <= x4 <= +inf

import lindo
import numpy as np
import os
#model data
nCons = 4
nVars = 4
nDir = 1
dObjConst = 0.0
adC = np.array([1.,1.,1.,1.],dtype=np.double)
adB = np.array([20.0,20.0,40.0,10.0],dtype=np.double)
acConTypes = np.array(['E','G','E','G'],dtype='|S1')
nNZ = 9
anBegCol = np.array([0,2,5,7,9],dtype=np.int32)
pnLenCol = np.asarray(None)
adA = np.array([3.0,4.0,6.0,5.0,7.0,8.0,1.0,2.0,9.0],dtype=np.double)
anRowX = np.array([0,2,1,2,3,2,3,0,1],dtype=np.int32)
pdLower = np.array([2,1,-lindo.LS_INFINITY,-lindo.LS_INFINITY],dtype=np.double)
pdUpper = np.array([5,lindo.LS_INFINITY,10,lindo.LS_INFINITY],dtype=np.double)

# The first try block is for catching errors rasied while creating an environment
try:
    #create LINDO environment and model objects
    LicenseKey = np.array('',dtype='S1024')
    lindo.pyLSloadLicenseString(os.getenv('LINDOAPI_HOME')+'/license/lndapi160.lic',LicenseKey)
    pnErrorCode = np.array([-1],dtype=np.int32)
    pEnv = lindo.pyLScreateEnv(pnErrorCode,LicenseKey)
except lindo.LINDO_Exception as e:
    print(e.args[0])
    exit(1)

# The Second try block is to catch errors rasied for the allocated LINDO enviroment
try:
    pModel = lindo.pyLScreateModel(pEnv,pnErrorCode)

  
    #load data into the model
    print("Loading LP data...")
    lindo.pyLSloadLPData(pModel,nCons,nVars,nDir,
                                    dObjConst,adC,adB,acConTypes,nNZ,anBegCol,
                                    pnLenCol,adA,anRowX,pdLower,pdUpper)

    #solve the model
    print("Solving the model...")
    pnStatus = np.array([-1],dtype=np.int32)
    lindo.pyLSoptimize(pModel,lindo.LS_METHOD_FREE,pnStatus)

    #retrieve the objective value
    dObj = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetInfo(pModel,lindo.LS_DINFO_POBJ,dObj)
    
    print("Objective is: %.5f" %dObj[0])

    #retrieve the primal solution and variable types
    varType = np.empty((nVars),dtype=np.byte)
    lindo.pyLSgetVarType(pModel,varType)

    padPrimal = np.empty((nVars),dtype=np.double)
    lindo.pyLSgetPrimalSolution(pModel,padPrimal)

    print("Primal solution is: ")
    for k,x in enumerate(padPrimal): 
        print("%.5f %c" % (padPrimal[k],varType[k]))
        
    #delete LINDO model pointer
    lindo.pyLSdeleteModel(pModel)

    #delete LINDO environment pointer
    lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")
