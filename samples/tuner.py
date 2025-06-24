###################################################################
#                       LINDO-API
#                    Sample Programs
#                  Copyright (c) 2001-2018
#
#         LINDO Systems, Inc.           312.988.7422
#         1415 North Dayton St.         info@lindo.com
#         Chicago, IL 60622             http://www.lindo.com
###################################################################
#  File   : Derived from samples/c/ex_tuner/ex_tuner.c
#  Purpose: Tuning parameters

import lindo
import numpy as np
import os

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

try:
    print(lindo.getversion(pEnv))

    dataPath = os.getenv('LINDOAPI_HOME') + "/samples/data"
    # Tuner instances */
    lindo.pyLSaddTunerInstance(pEnv, dataPath +"/bm23.mps.gz")

    lindo.pyLSaddTunerInstance(pEnv, dataPath +"/p0033.mps.gz")

    lindo.pyLSaddTunerInstance(pEnv, dataPath +"/p0201.mps.gz")

    lindo.pyLSaddTunerInstance(pEnv, dataPath +"/p0282.mps.gz")

    # Tuner options */
    lindo.pyLSaddTunerOption(pEnv,"max_parsets",6)
    lindo.pyLSaddTunerOption(pEnv,"use_gop",0)
    lindo.pyLSaddTunerOption(pEnv,"time_limit",10)
    lindo.pyLSaddTunerOption(pEnv,"ntrials",2)
    lindo.pyLSaddTunerOption(pEnv,"nthreads",1)
    lindo.pyLSaddTunerOption(pEnv,"seed",1032)
    lindo.pyLSaddTunerOption(pEnv,"criterion",1)

    # Tuner dynamic parameters */
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_IPARAM_LP_SCALE)
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_IPARAM_MIP_PRELEVEL)
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_IPARAM_MIP_BRANCHDIR)
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_IPARAM_MIP_BRANCHRULE)
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_IPARAM_MIP_FP_MODE)
    lindo.pyLSaddTunerZDynamic(pEnv,lindo.LS_DPARAM_SOLVER_FEASTOL)

    # Tuner static groups and parameters */
    lindo.pyLSaddTunerZStatic(pEnv,1,lindo.LS_IPARAM_MIP_NODESELRULE,4)
    lindo.pyLSaddTunerZStatic(pEnv,1,lindo.LS_DPARAM_MIP_RELINTTOL,0.0001)
    lindo.pyLSaddTunerZStatic(pEnv,1,lindo.LS_DPARAM_SOLVER_OPTTOL,1e-006)
    lindo.pyLSaddTunerZStatic(pEnv,2,lindo.LS_IPARAM_MIP_NODESELRULE,1)
    lindo.pyLSaddTunerZStatic(pEnv,2,lindo.LS_DPARAM_MIP_RELINTTOL,0.001)
    lindo.pyLSaddTunerZStatic(pEnv,2,lindo.LS_DPARAM_SOLVER_OPTTOL,1e-005)
    lindo.pyLSaddTunerZStatic(pEnv,3,lindo.LS_IPARAM_MIP_NODESELRULE,3)
    lindo.pyLSaddTunerZStatic(pEnv,3,lindo.LS_DPARAM_MIP_RELINTTOL,1e-005)
    lindo.pyLSaddTunerZStatic(pEnv,3,lindo.LS_DPARAM_SOLVER_OPTTOL,0.0001)

    lindo.pyLSprintTuner(pEnv)
    lindo.pyLSrunTuner(pEnv)

    lindo.pyLSdisplayTunerResults(pEnv)

    mCriterion = -1; #selected criterion
    jInstance  = -1; #avg instance
    lindo.pyLSwriteTunerParameters(pEnv,"lindo_tuned.par",jInstance,mCriterion)

    lindo.pyLSclearTuner(pEnv)

    #delete LINDO environment pointer
    lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")

