# Solve a multi-extremal continous model using GOP solver.
#
#           MINIMIZE      x * sin(x * pi)
#           subject to    0 <= x <= 10


import lindo
import numpy as np
import os

#Build instruction-list
#Number of constraints
ncons = 1
#Number of variables
nvars = 2
#Number of objectives
nobjs = 1
#Number of real number constants
nnums = 0
#Lower bounds of variables
lwrbnd = np.array([0.0, -2.0],dtype=np.double)
#Upper bounds of variables
uprbnd = np.array([10.0, 2.0],dtype=np.double)
#Starting point of variables
varval = np.array([0.0, 0.0],dtype=np.double)
numval = np.empty((nvars),dtype=np.double)
#Variable type
vtype = np.array(['C','C'],dtype='|S1')
#Count for instruction code
ikod = 0
#Count for objective row
iobj = 0
#Count for constraint row
icon = 0
# optional (paiVars)
varindex =  np.asarray(None)
#Instruction code of the objective
objsense = np.empty((10),dtype=np.int32)
objs_beg = np.empty((10),dtype=np.int32)
objs_length = np.empty((10),dtype=np.int32)
cons_beg = np.empty((10),dtype=np.int32)
cons_length = np.empty((10),dtype=np.int32)
code = np.empty((200),dtype=np.int32)
#Direction of optimization
objsense[iobj] = lindo.LS_MIN
#Beginning position of objective
objs_beg[iobj] = ikod
#Instruction list code
code[ikod] = lindo.EP_PUSH_VAR
ikod = ikod + 1
code[ikod] = 0
ikod = ikod + 1
code[ikod] = lindo.EP_PUSH_VAR
ikod = ikod + 1
code[ikod] = 0
ikod = ikod + 1
code[ikod] = lindo.EP_PI
ikod = ikod + 1
code[ikod] = lindo.EP_MULTIPLY
ikod = ikod + 1
code[ikod] = lindo.EP_SIN
ikod = ikod + 1
code[ikod] = lindo.EP_MULTIPLY
ikod = ikod + 1

#Length of objective
objs_length[iobj] = ikod - objs_beg[iobj]
iobj = iobj + 1

#Constraint type
ctype = np.array(['E'],dtype='|S1')
#Beginning position of constraint 0
cons_beg[icon] = ikod
#Instruction list code
code[ikod] = lindo.EP_PUSH_VAR
ikod = ikod + 1
code[ikod] = 1
ikod = ikod + 1

#Length of constraint 0
cons_length[icon] = ikod - cons_beg[icon]
icon = icon + 1

#Total number of items in the instruction list
lsize = ikod

# The first try block is for catching errors rasied while creating an environment
try:
    #create LINDO environment and model objects
    LicenseKey = np.array('',dtype='S1024')
    lindo.pyLSloadLicenseString(os.getenv('LINDOAPI_HOME')+'/license/lndapi150.lic',LicenseKey)
    pnErrorCode = np.array([-1],dtype=np.int32)
    pEnv = lindo.pyLScreateEnv(pnErrorCode,LicenseKey)
except lindo.LINDO_Exception as e:
    print(e.args[0])
    exit(1)

# The Second try block is to catch errors rasied for the allocated LINDO enviroment
try:
    pModel = lindo.pyLScreateModel(pEnv,pnErrorCode)

    #Set linearization level, before a call to LSloadNLPCode.
    nLinearz = 1 # No linearization occurs
    lindo.pyLSsetModelIntParameter(pModel,
                                   lindo.LS_IPARAM_NLP_LINEARZ,
                                   nLinearz)


    #Set up automatic differentiation, before a call to LSloadNLPCode.
    nAutoDeriv = 1 # Forward automatic differentiation
    lindo.pyLSsetModelIntParameter(pModel,
                                   lindo.LS_IPARAM_NLP_AUTODERIV,
                                   nAutoDeriv)


    #Load instruction list
    print("Loading instruction list...")
    
    lindo.pyLSloadInstruct(pModel, ncons, nobjs, nvars, nnums,
                           objsense, ctype, vtype, code, lsize,
                           varindex, numval, varval, objs_beg, objs_length,
                           cons_beg, cons_length, lwrbnd, uprbnd)


    #solve the model
    print("Solving the model...")
    pnStatus = np.array([-1],dtype=np.int32)
    lindo.pyLSsolveGOP(pModel, pnStatus)
    print(f"Solution status: {pnStatus[0]}\n")


    #retrieve the objective value
    dObj = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetInfo(pModel,lindo.LS_DINFO_POBJ,dObj)
    print(f"Objective is: {dObj[0]:.5f}\n")

    #retrieve the primal solution
    padPrimal = np.empty((nvars),dtype=np.double)
    lindo.pyLSgetPrimalSolution(pModel,padPrimal)
    print("Primal solution is: ")
    for x in padPrimal: print(f"{x:.5f}")

    #delete LINDO model pointer
    lindo.pyLSdeleteModel(pModel)


    #delete LINDO environment pointer
    lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")
