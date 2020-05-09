#!/usr/bin/python3import json
import requests, sys, re
import argparse
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: eQTL_Annotation.py
@time: 18-11-6 1:30
"""
import json
import requests, sys, re
import argparse

snppath = sys.argv[1]
snpfile = open(snppath)
outputpath = sys.argv[2]
Tissue = sys.argv[3]
output = open(outputpath,'a+')
outputpath2 = outputpath + ".id"
output2 = open(outputpath2,'a+')

def get_eqtl_hic_annotation(rsid,Tissue):
	server = "http://3dsnp.cbportal.org/api.do?id="+rsid+"&format=json&type=eqtl"
	r = requests.get(server,headers={"Content-Type" : "application/json"})
	if not r.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = r.content.decode()
	dict_decoded = json.loads(decoded)
	pos = ''
	chrom = ''
	eqtlgene = []
	eqtlplavue = []
	eqtlgenestring = ''
	eqtlplavuestring = ''
	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			if 'eqtl' in dict_decoded[i]:
				pos = dict_decoded[i]['position']
				chrom = dict_decoded[i]['chrom']
				eqtlstring = dict_decoded[i]['eqtl'].split(";")
				for query in eqtlstring:
					if Tissue in query:
						arr = query.split(',')
						eqtlgene.append(arr[0])
						eqtlplavue.append(arr[1])
	eqtlgenestring = ','.join(eqtlgene)
	eqtlplavuestring = ','.join(eqtlplavue)
	server = "http://3dsnp.cbportal.org/api.do?id="+rsid+"&format=json&type=3dsnp"
	r = requests.get(server,headers={"Content-Type" : "application/json"})
	if not r.ok:
		return 0
		#r.raise_for_status()
		#sys.exit()
	decoded = r.content.decode()
	dict_decoded = json.loads(decoded)
	hicgene = []
	#hicplavue = []
	hicgenestring = ''
	#hicplavuestring = ''
	if(len(dict_decoded)):
		for i in range(len(dict_decoded)):
			if 'data_loop_gene' in dict_decoded[i]:
				for j in range(len(dict_decoded[i]['data_loop_gene'])):
					if Tissue == dict_decoded[i]['data_loop_gene'][j]['loopCellTissue']:
						hicgene.append(dict_decoded[i]['data_loop_gene'][j]['loopGene'])

	temp = list(set(hicgene))
	hicgenestring = ','.join(temp)

	print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".\
		format(rsid,chrom,pos,eqtlgenestring,eqtlplavuestring,hicgenestring),file= output)
	for gene in hicgene+eqtlgene:
		print(gene,file= output2)

def main():
	snplists = []
	for oneline in snpfile:
		array = oneline.strip().split('\t')
		snplists.append(array[0])
	for rsid in snplists:
		get_eqtl_hic_annotation(rsid,Tissue)
	output.close()
	output2.close()

if __name__ == "__main__":
	sys.exit(main())


