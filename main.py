import freyjaSupport
import os


workingFolderEnv = os.environ.setdefault("WORKINGFOLDER", "/data")
if not os.path.isdir(workingFolderEnv):
    raise NotADirectoryError("Unable to find working directory at %s" %workingFolderEnv)
inputFolderEnv = os.environ.setdefault("INPUTFOLDER", os.path.join(workingFolderEnv, "freyjaOutput"))
if not os.path.isdir(inputFolderEnv):
    raise NotADirectoryError("Unable to find input folder at %s" %inputFolderEnv)
readGroupedFolderEnv = os.environ.setdefault("READGROUPEDFOLDER", os.path.join(workingFolderEnv, "rgBAM"))
freyjaOutputFolder = os.environ.setdefault("OUTPUTFOLDER", os.path.join(workingFolderEnv, "freyjaOutput"))
if not os.path.isdir(freyjaOutputFolder):
    os.mkdir(freyjaOutputFolder)


def getVCFList(folder:str=inputFolderEnv):
    folderContents = os.listdir(folder)
    folderFilesRaw = [os.path.join(folder, item) for item in folderContents]
    folderFilesFiltered = []
    for item in folderFilesRaw:
        if not os.path.isfile(item):
            continue
        if item.endswith(".vcf") or item.endswith(".vcf.gz"):
            folderFilesFiltered.append(item)
    return folderFilesFiltered


def findFreyjaStringentFilteredVCF(stringentFilteredVCFFolder:str=inputFolderEnv):
    if not os.path.isdir(stringentFilteredVCFFolder):
        raise NotADirectoryError("Unable to find input folder at %s" %stringentFilteredVCFFolder)
    vcfList = getVCFList(stringentFilteredVCFFolder)
    candidates = []
    for vcf in vcfList:
        if vcf.endswith(".freyjaMod.vcf"):
            candidates.append(vcf)
    if len(candidates) == 0:
        raise FileNotFoundError("Unable to find any .freyjaMod.vcf files in folder %s" %stringentFilteredVCFFolder)
    if len(candidates) > 1:
        raise RuntimeError("Found multiple .freyjaMod.vcf files in folder %s" %stringentFilteredVCFFolder)
    return os.path.join(stringentFilteredVCFFolder, candidates[0])


def findBAMFileForVariantCalling(bamFolder:str=readGroupedFolderEnv):
    if not os.path.isdir(bamFolder):
        raise NotADirectoryError("Unable to find BAM folder at %s" %bamFolder)
    bamList = os.listdir(bamFolder)
    candidates = []
    for bam in bamList:
        if bam.endswith(".bam"):
            candidates.append(bam)
    if len(candidates) == 0:
        raise FileNotFoundError("Unable to find any .bam files in folder %s" %bamFolder)
    if len(candidates) > 1:
        raise RuntimeError("Found multiple .bam files in folder %s" %bamFolder)
    return os.path.join(bamFolder, candidates[0])


def performFreyjaDemix(inputFolder:str=inputFolderEnv, outputFolder:str=freyjaOutputFolder):
    variantCallingBAMFile = findBAMFileForVariantCalling()
    stringentFilteredVCFFile = findFreyjaStringentFilteredVCF(inputFolder)
    variantTSV = freyjaSupport.tsvConvert.convertVCFtoTSV(stringentFilteredVCFFile, outputFolder)
    depthTSV = freyjaSupport.mpileupRunner.runMpileup(variantCallingBAMFile, outputFolder)
    freyjaOutputFile = freyjaSupport.catChariot.freyjaRunner(variantTSV, depthTSV, outputFolder)
    return freyjaOutputFile


if __name__ == "__main__":
    performFreyjaDemix()

