#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: Basic_Annotation.py
@time: 18-11-6 1:30
"""

# Basic Annotation of the data
import json
import requests, sys, re
import argparse

snppath = sys.argv[1]
snpfile = open(snppath)
outputpath = sys.argv[2]
Tissue = sys.argv[3]
output = open(outputpath,'a+')
outpath2 = outputpath + ".addition"
output2 = open(outpath2,'a+')
outpath3 = outputpath + ".id"
output3 = open(outpath3,'a+')
# function for single snp annotation 
# Step1, Add Ref|Alt & frequency information
# Step2，Add phyloP scores
# Step3， Add Linear nearst genes within 2kb range
def get_basic_annotation(rsID):
	server = "http://3dsnp.cbportal.org/api.do?id="+rsID+"&format=json&type=basic"
	r = requests.get(server,headers={"Content-Type" : "application/json"})
	if not r.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = r.content.decode()
	dict_decoded = json.loads(decoded)
	
	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			genes = []
			position = []
			rsid = dict_decoded[i]['id']
			pos = dict_decoded[i]['position']
			chrom = dict_decoded[i]['chrom']
			if 'MAF' in dict_decoded[i]:
				MAF = str(dict_decoded[i]['MAF'])
			Alt = dict_decoded[i]['Alt']
			Ref = dict_decoded[i]['Ref']
			AFR = dict_decoded[i]['AFR']
			AMR = dict_decoded[i]['AMR']
			EAS = dict_decoded[i]['EAS']
			EUR = dict_decoded[i]['EUR']
			SAS = dict_decoded[i]['SAS']
			if 'data_gene' in dict_decoded[i]:
				for j in range(len(dict_decoded[i]['data_gene'])):
					genes.append(dict_decoded[i]['data_gene'][j]['geneName'])
					position.append(dict_decoded[i]['data_gene'][j]['geneRelativePosition'])

			geneString = ','.join(genes)
			PosString = ','.join(position)

			for gene in genes:
				print(gene,file= output3)

			print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}".\
				  format(geneString,PosString,rsid,pos,chrom,MAF,Alt,Ref,MAF,AFR,AMR,EUR,SAS,EAS),file= output)

def get_tfbs_phylop_chromhmm(rsID,Tissue):
	servertfbs = "http://3dsnp.cbportal.org/api.do?id="+rsID+"&format=json&type=tfbs"
	rtfbs = requests.get(servertfbs,headers={"Content-Type" : "application/json"})
	if not rtfbs.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = rtfbs.content.decode()
	dict_decoded = json.loads(decoded)
	pos = ''
	chrom = ''
	tfbs = []
	tfbsString = ''
	phylop1 = 0
	phylop2 = 0
	chromstates = []
	chromstateString = ''

	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			pos = dict_decoded[i]['position']
			chrom = dict_decoded[i]['chrom']
			if 'data_tfbs' in dict_decoded[i]:
				for j in range(len(dict_decoded[i]['data_tfbs'])):
					if Tissue == dict_decoded[i]['data_tfbs'][j]['tfbsCellTissue']:
						tfbs.append(dict_decoded[i]['data_tfbs'][j]['tfbsFactor'])
	temp = list(set(tfbs))
	tfbsString = ','.join(temp)
	serverphylop = "http://3dsnp.cbportal.org/api.do?id="+rsID+"&format=json&type=phylop"
	rphylop = requests.get(serverphylop,headers={"Content-Type" : "application/json"})
	if not rphylop.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = rphylop.content.decode()
	dict_decoded = json.loads(decoded)
	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			string1 = dict_decoded[i]['physcores']
			string2 = dict_decoded[i]['physcores_update']
			arr1 = string1.split(',')
			arr2 = string2.split(',')
			phylop1 = arr1[10]
			phylop2 = arr2[10]
	serverchromhmm = "http://3dsnp.cbportal.org/api.do?id="+rsID+"&format=json&type=chromhmm"
	rchromhmm = requests.get(serverchromhmm,headers={"Content-Type" : "application/json"})
	if not rchromhmm.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = rchromhmm.content.decode()
	dict_decoded = json.loads(decoded)
	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			if 'data_chromhmm' in dict_decoded[i]:
				for j in range(len(dict_decoded[i]['data_chromhmm'])):
					if 'chromhmmTissue' in dict_decoded[i]['data_chromhmm'][j]:
						if Tissue == dict_decoded[i]['data_chromhmm'][j]['chromhmmTissue']:
							chromstates.append(dict_decoded[i]['data_chromhmm'][j]['chromhmmName'])
	temp = list(set(chromstates))
	chromstateString = ','.join(temp)
	
	print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".\
		format(rsID,pos,chrom,tfbsString,phylop1,phylop2,chromstateString),file= output2)


def main():
	snplists = []
	for oneline in snpfile:
		array = oneline.strip().split('\t')
		snplists.append(array[0])
	for rsid in snplists:
		get_basic_annotation(rsid)
		get_tfbs_phylop_chromhmm(rsid,Tissue)
	output.close()
	output2.close()
	output3.close()
if __name__ == "__main__":
	sys.exit(main())