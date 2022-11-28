def test_pyLindo_version():
    
    import lindo
    import numpy as np
    import os


    import lindo
    import numpy as np
    import os
    #TODO: remove hardcoded version tags, e.g. 14.0 -> LS_IPARAM_VER_MAJOR.LS_IPARAM_VER_MINOR
    pnErrorCode = np.array([-1],dtype=np.int32)
    licPath = os.getenv('LINDOAPI_HOME')+'/license/lndapi140.lic' 
    try:
        LicenseKey = np.array([''],dtype='S1024')
        lindo.pyLSloadLicenseString(licPath,LicenseKey)
        pEnv = lindo.pyLScreateEnv(pnErrorCode,LicenseKey)
        lindo.pyLSdeleteEnv(pEnv)
        print("The Lindo API 14.0 Python interface is working.")
    except lindo.LINDO_Exception as e:
        if(e.args[1] == lindo.LSERR_NO_VALID_LICENSE):
            print(f"{e.args[1]} => Unable to load license at {licPath}")
        else:
            print(e.args[0])