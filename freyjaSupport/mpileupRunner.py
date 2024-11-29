import os


SAMTOOLSPATH = "/opt/conda/envs/freyja-env/bin/samtools"
referenceGenomeEnv = os.environ.setdefault("REFGENOME", "/root/references/Sars_cov_2.ASM985889v3.dna_sm.toplevel.fa")



def runMpileup(inputBAM:str, outputFolder:str):
    outputFileName = os.path.split(inputBAM)[1][:-4] + ".depth.tsv"
    outputFile = os.path.join(outputFolder, outputFileName)
    mpileupCMD = "%s mpileup -aa -A -d 0 -B -Q 0 --reference %s %s | cut -f1-4 > %s" % (SAMTOOLSPATH, referenceGenomeEnv, inputBAM, outputFile)
    print("RUN: %s" % mpileupCMD, flush=True)
    statusCode = os.system(mpileupCMD)
    if statusCode != 0:
        raise RuntimeError("Mpileup failed with status code %s" % statusCode)
    return outputFile
