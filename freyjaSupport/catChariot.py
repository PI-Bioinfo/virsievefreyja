import os


FREYJAPATH = "/opt/conda/envs/freyja-env/bin/freyja"


def freyjaRunner(variantTSV, depthTSV, outputFolder):
    outputFileName = os.path.split(variantTSV)[1][:-4] + ".freyjaDemix"
    outputFile = os.path.join(outputFolder, outputFileName)
    freyjaCMD = "%s demix %s %s --output %s" % (FREYJAPATH, variantTSV, depthTSV, outputFile)
    print("RUN: %s" %freyjaCMD, flush=True)
    statusCode = os.system(freyjaCMD)
    if statusCode != 0:
        raise RuntimeError("Freyja failed with status code %s" % statusCode)
    return outputFile