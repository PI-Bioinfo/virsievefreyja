import os


VCF2TSVPATH = "/opt/conda/envs/freyja-env/bin/vcf2tsvpy"


def convertVCFtoTSV(inputVCF, outputFolder):
    outputFileName = os.path.split(inputVCF)[1][:-4] + ".tsv"
    outputFile = os.path.join(outputFolder, outputFileName)
    convertCMD = "%s --input %s --out_tsv %s" % (VCF2TSVPATH, inputVCF, outputFile)
    print("RUN: %s" %convertCMD, flush=True)
    statusCode = os.system(convertCMD)
    if statusCode != 0:
        raise RuntimeError("VCF to TSV conversion failed with status code %s" % statusCode)
    sedCMD = "sed -i '/^#/d' %s" % outputFile
    print("RUN: %s" %sedCMD, flush=True)
    statusCode = os.system(sedCMD)
    if statusCode != 0:
        raise RuntimeError("SED command failed with status code %s" % statusCode)
    return outputFile