#  Stochastic Programming Version of an American Put Option as a
#  six period model.
#
#  The holder of the option has the right to sell a specified stock
#  at any time(the American feature) between now and a specified
#  expiration date at a specified strike price.
#  The holder makes a profit in the period of exercise if the
#  strike price exceeds the market price of the stock at the
#  time of sale.  Wealth is invested at the risk free rate.
#
#  Initial Price  = $100
#  Strike price   =  $99
#  Risk free rate = 0.04%
#
#
#   MODEL:
#   [OBJ] MAX= W5 ;
#
#   [INITIAL]        P0 = 100 ;    !price at t=0;
#   [R0000001] RV0 * P0 = P1  ;    !price at t=1;
#   [R0000003] RV1 * P1 = P2  ;    !price at t=2;
#   [R0000005] RV2 * P2 = P3  ;    !price at t=3;
#   [R0000007] RV3 * P3 = P4  ;    !price at t=4;
#   [R0000009] RV4 * P4 = P5  ;    !price at t=5;
#
#   [R0000000]           + Y0 * ( 99 - P0) = W0  ;  !wealth at t=0;
#   [R0000002] 1.04 * W0 + Y1 * ( 99 - P1) = W1  ;  !wealth at t=1;
#   [R0000004] 1.04 * W1 + Y2 * ( 99 - P2) = W2  ;  !wealth at t=2;
#   [R0000006] 1.04 * W2 + Y3 * ( 99 - P3) = W3  ;  !wealth at t=3;
#   [R0000008] 1.04 * W3 + Y4 * ( 99 - P4) = W4  ;  !wealth at t=4;
#   [R0000010] 1.04 * W4 + Y5 * ( 99 - P5) = W5  ;  !wealth at t=5;
#
#   [R0000011] Y0 + Y1+ Y2+ Y3 + Y4 +  Y5 <= 1 ; ! sell only once;
#
#   @FREE(Wt); t=0..5;
#   @FREE(Pt); t=0..5;
#   @BIN(Yt); t=0..5;
#
#  Stochastic Parameters:
#  RVt : random return in the end of period t, for t=0..4
#
#  Decision Variables:
#  Pt: Price of option in the beginning of period t, for t=0..5
#  Wt: Wealth int the beginning of period t, for t=0..5
#  Yt: 1 if sold in the beginning of period t, 0 otherwise, for t=0..5
#
#  Objective: maximize the wealth at the beginning of period 5 (i.e.
#             end of planning horizon).   

from platform import system
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
    pModel = lindo.pyLScreateModel(pEnv,pnErrorCode)

 

    mpiFn = "smpi/putoption.mpi"
    lindo.pyLSreadMPIFile(pModel,mpiFn)


    #Load stage/time structure for rows,columns and stochastic params
    numStages = 6
    colStages = np.array([5,0,1,2,3,4,5,0,0,1,1,2,2,3,3,4,4,5,-1],dtype=np.int32)
    rowStages = np.array([0,1,3,5,2,4,0,2,4,1,3,5,5,-1],dtype=np.int32)
    panSparStage = np.array([1,2,3,4,5,-1],dtype=np.int32)
    padSparValue = np.array([0,0,0,0,0,-1],dtype=np.double)
    lindo.pyLSloadStageData(pModel,numStages, rowStages,colStages)
    lindo.pyLSloadStocParData(pModel,panSparStage,padSparValue)


    #Load stochastic data
    iStage = 1
    nBlockEvents = 4
    iModifyRule = lindo.LS_REPLACE
    padProb = np.array([0.25,0.25,0.25,0.25,-1],dtype=np.double)
    pakStart = np.array([0,1,2,3,4,-1],dtype=np.int32)
    paiRows = np.asarray(None)
    paiCols = np.asarray(None)
    paiStvs = np.array([0,0,0,0,-1],dtype=np.int32)
    padVals = np.array([-0.08,0.01,0.07,0.11,-1],dtype=np.double)
    lindo.pyLSaddDiscreteBlocks(pModel,iStage, nBlockEvents,padProb,
                                pakStart,paiRows, paiCols,paiStvs,
                                padVals,iModifyRule)

    iStage = 2
    nBlockEvents = 2
    iModifyRule = lindo.LS_REPLACE
    padProb = np.array([0.5,0.5,-1],dtype=np.double)
    pakStart = np.array([0,1,2,-1],dtype=np.int32)
    paiRows = np.asarray(None)
    paiCols = np.asarray(None)
    paiStvs = np.array([1,1,-1],dtype=np.int32)
    padVals = np.array([-0.08,0.01,-1],dtype=np.double)
    lindo.pyLSaddDiscreteBlocks(pModel,iStage, nBlockEvents,padProb, pakStart,paiRows,
                                paiCols,paiStvs, padVals,iModifyRule)

    iStage = 3
    nBlockEvents = 2
    iModifyRule = lindo.LS_REPLACE
    padProb = np.array([0.5,0.5,-1],dtype=np.double)
    pakStart = np.array([0,1,2,-1],dtype=np.int32)
    paiRows = np.asarray(None)
    paiCols = np.asarray(None)
    paiStvs = np.array([2,2,-1],dtype=np.int32)
    padVals = np.array([0.07,0.11,-1],dtype=np.double)
    lindo.pyLSaddDiscreteBlocks(pModel,iStage, nBlockEvents,padProb, pakStart,paiRows,
                                paiCols, paiStvs, padVals, iModifyRule)


    iStage = 4
    nBlockEvents = 2
    iModifyRule = lindo.LS_REPLACE
    padProb = np.array([0.5,0.5,-1],dtype=np.double)
    pakStart = np.array([0,1,2,-1],dtype=np.int32)
    paiRows = np.asarray(None)
    paiCols = np.asarray(None)
    paiStvs = np.array([3,3,-1],dtype=np.int32)
    padVals = np.array([0.01,0.11,-1],dtype=np.double)
    lindo.pyLSaddDiscreteBlocks(pModel,iStage, nBlockEvents,padProb, pakStart,
                                paiRows, paiCols,paiStvs, padVals,iModifyRule)

    iStage = 5
    nBlockEvents = 2
    iModifyRule = lindo.LS_REPLACE
    padProb = np.array([0.5,0.5,-1],dtype=np.double)
    pakStart = np.array([0,1,2,-1],dtype=np.int32)
    paiRows = np.asarray(None)
    paiCols = np.asarray(None)
    paiStvs = np.array([4,4,-1],dtype=np.int32)
    padVals = np.array([-0.08,0.07,-1],dtype=np.double)
    lindo.pyLSaddDiscreteBlocks(pModel,iStage, nBlockEvents,padProb,pakStart,paiRows,
                                paiCols,paiStvs, padVals,iModifyRule)


    #Get and display SP statistics
    numVars = np.array([-1],dtype=np.int32)
    lindo.pyLSgetInfo(pModel, lindo.LS_IINFO_NUM_VARS, numVars)

    numCons = np.array([-1],dtype=np.int32)
    lindo.pyLSgetInfo(pModel, lindo.LS_IINFO_NUM_CONS, numCons)

    numCont = np.array([-1],dtype=np.int32)
    lindo.pyLSgetInfo(pModel, lindo.LS_IINFO_NUM_CONT, numCont)

    numStocPars = np.array([-1],dtype=np.int32)
    lindo.pyLSgetInfo(pModel, lindo.LS_IINFO_NUM_SPARS, numStocPars)

    numStages = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_STAGES, 0, numStages)

    numNodes = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_NODES, 0, numNodes)

    numScens = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_SCENARIOS,0, numScens)

    numDeqRows = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_ROWS_DETEQI, 0, numDeqRows)

    numDeqCols = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_COLS_DETEQI,0,numDeqCols)

    numCoreRows = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_ROWS_CORE,0, numCoreRows)

    numCoreCols = np.array([-1],dtype=np.int32)
    lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_COLS_CORE, 0, numCoreCols)

    print("\nStochastic Model Stats:")
    print(f"Number of stages = {numStages[0]}")
    print(f"Number of nodes = {numNodes[0]}")
    print(f"Number of scenarios = {numScens[0]}")
    print(f"Core model (rows,cols) = ({numCoreRows[0]},{numCoreCols[0]})\n")

    numStageRows = np.array([-1],dtype=np.int32)
    numStageCols = np.array([-1],dtype=np.int32)
    for i in range(0,numStages[0]):
        lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_ROWS_STAGE, i, numStageRows)
        lindo.pyLSgetStocInfo(pModel, lindo.LS_IINFO_STOC_NUM_COLS_STAGE, i, numStageCols)
        print(f"Core model (rows,col) in stage {i}: ({numStageRows},{numStageCols})")

    print(f"Deterministic eq. (rows,col) = ({numDeqRows[0]},{numDeqCols[0]})\n")

    noLinearization = 1
    lindo.pyLSsetModelIntParameter(pModel, lindo.LS_IPARAM_NLP_LINEARZ, noLinearization)
    
    #Solve the SP
    nStatus = np.array([-1],dtype=np.int32)
    lindo.pyLSsolveSP(pModel,nStatus)

    #Access the final solution if optimal or feasible
    if (nStatus[0] == lindo.LS_STATUS_OPTIMAL or
        nStatus[0] == lindo.LS_STATUS_BASIC_OPTIMAL or
        nStatus[0] == lindo.LS_STATUS_LOCAL_OPTIMAL or
        nStatus[0] == lindo.LS_STATUS_FEASIBLE
        ):
        dObj = np.array([-1.0],dtype=np.double)
        lindo.pyLSgetStocInfo(pModel, lindo.LS_DINFO_STOC_EVOBJ, 0, dObj)

        print(f"Objective  = {dObj[0]:.5f}")
    else:
        print(f"Optimization failed. nStatus = {nStatus[0]}" )

    #delete LINDO model pointer
    lindo.pyLSdeleteModel(pModel)

    #delete LINDO environment pointer
    lindo.pyLSdeleteEnv(pEnv)

except lindo.LINDO_Exception as e:
    lindo.geterrormessage(pEnv, e.args[1])
except Exception as e:
    print(f"Other Error => {e}")

