#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: main.py
@time: 18-11-6 1:30
"""
import json
import requests, sys, re
import argparse
import os

parser = argparse.ArgumentParser(description="Annotation of Variations with VarGeneNetEntropy.")
parser.add_argument("-P","--path", help = "Annotation File Path URL",
				default = "./dataset/")
parser.add_argument("-I", "--input", help ="Input File")
parser.add_argument("-LD","--ld",type=int,choices=[0,1],
				help = "1: LD extension ;0, No LD extension.",
				default = 0)
parser.add_argument("-H","--eqtlhic",type=int,choices=[0,1],
				help = "1: eQTL + HiC Annotation;0, No eQTL + HiC Annotation.",
				default = 1)
parser.add_argument("-G","--gsea",type=int,choices=[0,1],
				help = "1:GSEA Annalysis;0, No GSEA Annalysis.",
				default = 1)
parser.add_argument("-E","--entropy",type=int,choices=[0,1],
				help = "1:GSEA Annalysis;0, No GSEA Annalysis.",
				default = 1)
parser.add_argument("-D","--efo",
				help = "EFO Diseases ID.")
parser.add_argument("-S","--sample",
				help = "Sample Name.",
				default = "Test_sample")
parser.add_argument("-T","--tissue",
				help = "Tissue Name.")


args = parser.parse_args()

DataUrl = args.path
SnpPath = args.input
LDchoice = args.ld
HigerAnno = args.eqtlhic
GseaChoice = args.gsea
SampleName = args.sample
EfoName = args.efo
EntrpyChoice = args.entropy
Tissue = args.tissue

outdir = SampleName + "_result"

os.system("mkdir "+outdir)

# Step1: Download dataset or use your input.
if EfoName :
	os.system("python3 " + "./src/download_from_Gwascatalog.py " + EfoName + " ./" +outdir +"/"+SampleName+"_download.txt")

# Step2: LD extension.
if LDchoice:
	os.system("python3 " + "./src/LD_extension.py " + outdir +"/"+SampleName+"_download.txt" + " " + outdir +"/"+SampleName+"_ldextension.txt")

# Step3: Basic annotation.
if LDchoice:
	SnpPath = outdir +"/"+SampleName+"_ldextension.txt"
elif EfoName:
	SnpPath = outdir +"/"+SampleName+"_download.txt"

os.system("python3 " + "./src/Basic_Annotation.py " + " " + SnpPath + " " +outdir + "/" + SampleName + "_basic.genes.txt" + " " + Tissue)

# Step4: eQTL annotaion + HiC Annotation.
if HigerAnno:
	os.system("python3 " + "./src/eQTL_Annotation.py " + " " + SnpPath + " " + outdir + "/" + SampleName + "_eqtl_hic.genes.txt" + " " + Tissue  )


# Step5: Cat the genes and dedup.

os.system("cat " + outdir + "/*.id |grep -v ? > " + outdir + "/AllGenesID.txt")

# Step6: Pathway Annotation 
if GseaChoice or EntrpyChoice:
	os.system("python3 ./src/PathwayAnnotation.py "+ outdir + "/AllGenesID.txt " + SampleName)

