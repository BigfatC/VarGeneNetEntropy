#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: PathwayAnnotation.py
@time: 18-11-10 2:30
"""

import sys
import re
from scipy import stats
import requests
import math

# File Path Config
GeneFilePath = sys.argv[1]
SampleName = sys.argv[2]

GeneIdFile = open(GeneFilePath)

GeneList = []

for oneline in GeneIdFile:
	geneid = oneline.strip('\n')
	GeneList.append(geneid)

AnnotationFile = open("./datasets/all.gmt")

OutFile = open(SampleName+"_result/PathwayAnnoation.txt","w+")

# GeneSets Number Parameters
NGenes = 37717
nGenes = len(GeneList)
KGenes = 0
kGenes = 0


def accSum(n):
	sum =0
	for i in range(1,n+1):
		sum += i
	return sum

def CalculateGSEA(k,N,n,K):
	odds = stats.hypergeom.pmf(k,N,n,K)
	return odds

def getPPI(my_genes,threshold):
	string_api_url = "https://string-db.org/api"
	output_format = "tsv-no-header"
	method = "network"

	##
	## Construct URL
	##

	request_url = "/".join([string_api_url, output_format, method])

	##
	## Set parameters. 
	##

	#my_genes = ["CDC42","CDK1","KIF23","PLK1",
	#            "RAC2","RACGAP1","RHOA","RHOB"]

	params = {

		"identifiers" : "%0d".join(my_genes), # your protein
		"species" : 9606, # species NCBI identifier 
		"caller_identity" : "www.awesome_app.org" # your app name

	}

	##
	## Call STRING
	##

	response = requests.post(request_url, data=params)
	templist = []
	for line in response.text.strip().split("\n"):
		#print(line)
		l = line.strip().split("\t")
		if len(l) < 5:
			break
		p1, p2 = l[2], l[3]

		## filter the interaction according to total score
		experimental_score = float(l[5])
		if experimental_score > threshold and p1 in my_genes and p2 in my_genes: 
			templist.append(experimental_score)
		else:
		   templist.append(float(threshold))

	return templist

def calculateEntropy(geneInSet,GeneInBackground,threshold):

	TotalLen = accSum(len(GeneInBackground)-1)

	localx = getPPI(geneInSet,threshold)
	globalx = getPPI(GeneInBackground,threshold)
	temp1 = 0
	temp2 = 0

	for PPI in localx:
		temp1 -= PPI * math.log(PPI)
	temp1 -= (TotalLen-len(localx))*threshold* math.log(threshold)

	for PPI in globalx:
		temp2 -= PPI * math.log(PPI)
	temp2 -= (TotalLen-len(globalx))*threshold* math.log(threshold)
	#rint(temp1)
	#print(temp2)
	#print(TotalLen)
	#print(len(globalx))
	Evalue = float(-math.log(temp2/temp1))
	return Evalue
 
def main():
	counts = 0
	tempGenes = []
	for oneline in AnnotationFile:
		line = oneline.strip('\n')
		array = re.split('\t',line)
		PathwayName = array[0]
		PathwayInfo = array[1]
		for hugoid in GeneList:
			if hugoid in array:
				counts += 1
				tempGenes.append(hugoid)
		if counts > 1 :
			kGenes = counts
			KGenes = len(array) - 2
			PGSEA = CalculateGSEA(kGenes,NGenes,nGenes,KGenes)
			if PGSEA < 1e-5:
				Evalue = calculateEntropy(tempGenes,array[2:],0.4)
				print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".\
					format(PathwayName,PathwayInfo,PGSEA,Evalue,kGenes,KGenes,','.join(tempGenes)),file=OutFile)

		tempGenes=[]
		counts = 0

	OutFile.close()

if __name__ == "__main__":
	sys.exit(main())