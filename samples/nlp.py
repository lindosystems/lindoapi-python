###################################################################
#                       LINDO-API
#                    Sample Programs
#                  Copyright (c) 2011
#
#         LINDO Systems, Inc.           312.988.7422
#         1415 North Dayton St.         info@lindo.com
#         Chicago, IL 60622             http://www.lindo.com
###################################################################
#
#  File   : Derived from samples/c/ex_nlp1/ex_nlp1.c
#
#  Purpose: Solve a NLP using the black-box style interface.
#  Model  : A nonlinear model with multiple local minimizers.
#
#        minimize  f(x,y) =  3*(1-x)^2*exp(-(x^2) - (y+1)^2)
#                         - 10*(x/5 - x^3 - y^5)*exp(-(x^2)-y^2)
#                         - 1/3*exp(-((x+1)^2) - y^2)
#        subject to
#                         x^2 + y   <=  6
#                         x   + y^2 <=  6
#                         x, y unconstrained in sign
import lindo
import numpy as np
import math
import os
import sys

####
##
def logFunc(pModel,line, udict): 
    print("%s" % (line),end =" ")

####
##
def cbFunc(pModel,iloc, udict): 
    dObj = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,iloc,lindo.LS_DINFO_CUR_OBJ,dObj)
    dIter = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,iloc,lindo.LS_DINFO_CUR_ITER,dIter)    
    print("\ncbFunc| LOC:%d Iter:%g, Obj=%g" % (iloc,dIter[0],dObj[0]),end =" ")

####
##
def cbMIPFunc(pModel,udict,dObj,padPrimal):     
    dIter = np.array([-1.0],dtype=np.double)
    lindo.pyLSgetProgressInfo(pModel,0,lindo.LS_DINFO_CUR_ITER,dIter)    
    print("\ncbMIPFunc| Iter:%g, Obj=%g" % (dIter[0],dObj,),end =" ")
    for k,x in enumerate(padPrimal): 
        print("\n%.5f %s" % (padPrimal[k],udict["varType"][k]),end=" ")

  
####
## FDE calculations
# Function evals
def  g1(X,Y): return math.exp( -pow(X  ,2)  - pow(Y+1,2) )  
def  g2(X,Y): return math.exp( -pow(X  ,2)  - pow(Y  ,2) )  
def  g3(X,Y): return math.exp( -pow(X+1,2)  - pow(Y  ,2) )  
def  f1(X,Y): return pow(1-X,2)                        
def  f2(X,Y): return X/5 - pow(X  ,3)  - pow(Y  ,5)   
               
# Partial derivatives of the summands  (only to be used with cbGradcalc)
def dxg1(X,Y): return ( g1(X,Y)*(-2)*X     )
def dyg1(X,Y): return ( g1(X,Y)*(-2)*(Y+1) )
def dxg2(X,Y): return ( g2(X,Y)*(-2)*X     )
def dyg2(X,Y): return ( g2(X,Y)*(-2)*Y     )
def dxg3(X,Y): return ( g3(X,Y)*(-2)*(X+1) )
def dyg3(X,Y): return ( g3(X,Y)*(-2)*Y     )
def dxf1(X,Y): return ( 2*(1-X)            )
def dyf1(X,Y): return ( 0                  )
def dxf2(X,Y): return ( 1/5 - 3*pow(X,2)   )
def dyf2(X,Y): return ( -5*pow(Y,4)        )
               
def cbFuncalc(pModel,udict,nRow,padPrimal,nJDiff,dXJBase,pyFuncVal,pReserved):
  nerr = 0
  # compute objective's functional value*/
  X = padPrimal[0]
  Y = padPrimal[1]
  if (nRow==-1):
    val = 3*f1(X,Y)*g1(X,Y) - 10*f2(X,Y)*g2(X,Y) - g3(X,Y)/3
  # compute constaint 0's functional value */
  elif (nRow==0):
    val = X*X + Y - 6.0
  # compute constaint 1's functional value */
  elif (nRow==1):
    val = X + Y*Y - 6.0
    
  pyFuncVal[0]=val  
  udict["nfunc"] = udict["nfunc"] + 1
  return nerr

def cbGradcalc(pModel,udict,nRow,pdX,lb,ub,NewPnt,NPar,parlist,partial):
  nerr = 0
  # compute objective's gradient values*/  
  X = padPrimal[0]
  Y = padPrimal[1]
  
  for i2 in range(NPar): partial[i2]=0.0
  
  # partial derivatives of the objective function */
  if (nRow==-1):
     for i2 in range(NPar):
       if (lb[parlist[i2]]!=ub[parlist[i2]]):
           if (parlist[i2]==0):
             partial[i2]= 3*(dxf1(X,Y)*g1(X,Y) + f1(X,Y)*dxg1(X,Y) ) -  10*(dxf2(X,Y)*g2(X,Y) + f2(X,Y)*dxg2(X,Y) ) - 1/3*(dxg3(X,Y))
           elif (parlist[i2]==1):
             partial[i2]= 3*(dyf1(X,Y)*g1(X,Y) + f1(X,Y)*dyg1(X,Y) ) -  10*(dyf2(X,Y)*g2(X,Y) + f2(X,Y)*dyg2(X,Y) ) - 1/3*(dyg3(X,Y))
                       
  # partial derivatives of Constraint 0 */
  elif (nRow==0):
     for i2 in range(NPar):
       if (lb[parlist[i2]]!=ub[parlist[i2]]):
         if (parlist[i2]==0):
           partial[i2]=2.0*X
         elif (parlist[i2]==1):
           partial[i2]=1
         
  # partial derivatives of Constraint 1 */
  elif (nRow==1):
     for i2 in range(NPar):
       if (lb[parlist[i2]]!=ub[parlist[i2]]):
         if (parlist[i2]==0):
           partial[i2]=1
         elif (parlist[i2]==1):
           partial[i2]=2.0*Y
  udict["ngrad"] = udict["ngrad"] + 1
  return nerr
  
####################################
## MAIN    
####################################
#model LP data
nCons = 2
nVars = 2
nDir = 1
dObjConst = 0.0
adC = np.array([0.0,0.0],dtype=np.double)
adB = np.array([0.0,0.0],dtype=np.double)
acConTypes = np.array(['L','L'],dtype='|S1')
nNZ = 4
Abegcol = np.array([0,2,4],dtype=np.int32)
Alencol = np.array([2,2],dtype=np.int32)
Acoef = np.array([0.,1.,1.,0.],dtype=np.double)
Arowndx = np.array([0,1,0,1],dtype=np.int32)
lb = np.array([-3.,-3.],dtype=np.double)
ub = np.array([3.,3.],dtype=np.double)
pachVarType = np.array(['C','C'],dtype='|S1')
# NLP data
Nobjndx = np.array([0,1],dtype=np.int32)
Nnlobj = 2

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
  verstr = lindo.getversion(pEnv)

  pModel = lindo.pyLScreateModel(pEnv,pnErrorCode)


  #load LP data into the model
  print("Loading LP data...")
  lindo.pyLSloadLPData(pModel,nCons,nVars,nDir,
                       dObjConst,adC,adB,acConTypes,nNZ,Abegcol,
                       Alencol,Acoef,Arowndx,lb,ub)

  lindo.pyLSloadVarType(pModel,pachVarType)

  #load NLP data
  # The number of nonlinear variables in each column 
  Alencol[0]=1 
  Alencol[1]=1

  # The indices of the first nonlinear variable in each column 
  Abegcol[0]=0 
  Abegcol[1]=1 
  Abegcol[2]=2

  # The indices of nonlinear constraints 
  Arowndx[0]=0
  Arowndx[1]=1

  lindo.pyLSloadNLPData(pModel,Abegcol,Alencol,
          np.asarray(None),Arowndx,Nnlobj,Nobjndx,np.asarray(None))
  
  ###############################
  ## Set callbacks 
  udict = {
    "prefix": "APILOG",
    "postfix": "..",
    "version": verstr,
    "varType": pachVarType,
    "ngrad": 0,
    "nfunc": 0
  }
  lindo.pyLSsetModelLogfunc(pModel,logFunc, udict)

  lindo.pyLSsetFuncalc(pModel,cbFuncalc, udict)

  lindo.pyLSsetGradcalc(pModel,cbGradcalc, udict)

  # Set maximum number of local optimizations */
  lindo.pyLSsetModelIntParameter(pModel,lindo.LS_IPARAM_NLP_MAXLOCALSEARCH,5)

  ###############################
  # Get model stats  
  ibuf = np.array([1],dtype=np.int32)
  lindo.pyLSgetInfo(pModel,lindo.LS_IINFO_NUM_CONT,ibuf) # number of continuous variables
  nCont = ibuf[0] 

  #####################################
  ## Load initial solution
  padPrimal = np.empty((nVars),dtype=np.double)
  padPrimal[0] = 0.25  
  padPrimal[1] = -1.65
  lindo.pyLSloadVarStartPoint(pModel,padPrimal)

  #####################################
  ## Solve the model
  print("Solving the model...")
  pnStatus = np.array([-1],dtype=np.int32)
  if nCont<nVars:
      lindo.pyLSsolveMIP(pModel,pnStatus)
  else:
      lindo.pyLSoptimize(pModel,lindo.LS_METHOD_FREE, pnStatus)    

  #####################################
  ## Retrieve the objective value
  dObj = np.array([-1.0],dtype=np.double)
  if nCont<nVars:
      lindo.pyLSgetInfo(pModel,lindo.LS_DINFO_MIP_OBJ,dObj)
  else:
      lindo.pyLSgetInfo(pModel,lindo.LS_DINFO_POBJ,dObj)    

  #####################################
  ## Retrieve the primal solution
  if nCont<nVars:
      lindo.pyLSgetMIPPrimalSolution(pModel,padPrimal)
  else:
      lindo.pyLSgetPrimalSolution(pModel,padPrimal)    

  varType = np.empty((nVars),dtype=np.byte)
  lindo.pyLSgetVarType(pModel,varType)

  print("Primal solution is: ")
  for k,x in enumerate(padPrimal): 
      print("x[%d] =%10.5f %c" % (k,padPrimal[k],varType[k]))
  print(f"Objective is: %.5f (nfunc:%d, ngrad:%d)" % (dObj[0],udict["nfunc"],udict["ngrad"]))
  ################################    
  # Delete LINDO model pointer
  lindo.pyLSdeleteModel(pModel)
  ################################
  # Delete LINDO environment pointer
  lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")