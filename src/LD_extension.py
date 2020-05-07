#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: LD_extension.py
@time: 18-12-12 22:09
"""

import json
import requests, sys, re
import argparse

inPath = sys.argv[1]
outPath = sys.argv[2]
infile = open(inPath)
outfile = open(outPath,'a+')

def get_pair_LD(rs1,rs2,population):
	
	"""
	Get LD score for a pair of SNPs
	"""
    server = "https://rest.ensembl.org"
    ext = "/ld/human/pairwise/"+rs1+"/"+rs2+"?population_name=1000GENOMES:phase_3:"+population
 
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
    if not r.ok:
      #r.raise_for_status()
      return 0
 
    decoded = r.content.decode()
    dict_decoded = json.loads(decoded)
    if len(dict_decoded):
        r2 = dict_decoded[0]['r2']
        population = dict_decoded[0]['population_name']
        print("{0}\t{1}\t{2}\t{3}".format(rs1,rs2,population,r2))
        return r2
    else:
        print('No message')
        return 0

def get_related_variants(rsID,r2_threshold,population):
	"""
	Get related variants for a single SNP
	"""
    server = "https://rest.ensembl.org"
    ext = "/ld/human/"+rsID+"/1000GENOMES:phase_3:"+population+"?"+"r2="+str(r2_threshold)\
        + "?window_size="+"20"
 
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
    if not r.ok:
      #r.raise_for_status()
      #sys.exit()
        return []
    
    decoded = r.content.decode()
    dict_decoded = json.loads(decoded)
    len_snp = len(dict_decoded)
    target = []
    if len_snp:
        for i in range(len_snp):
            r2 = dict_decoded[i]['r2']
            rsid1 = dict_decoded[i]['variation1']
            rsid2 = dict_decoded[i]['variation2']
            d_prime = dict_decoded[i]['d_prime']
            print("{0}\t{1}\t{2}\t{3}\t{4}".format(rsid1,rsid2,population,r2,d_prime),file= outfile)
            target.append(rsid2)
    return target

def select_Indipendent_snp(rsIDlist,threshold):
    count = 0
    Ind_snp_list = []
    for rsid1 in rsIDlist:
        count = 0
        for rsid2 in rsIDlist:
            count+=1
            if rsid1 != rsid2:
                if float(get_pair_LD(rsid1,rsid2,"CHB")) > threshold:
                    break
            if count == len(rsIDlist):
                Ind_snp_list.append(rsid1)
        
    return Ind_snp_list

def main():

	rsIDTemp = []
	for oneline in infile:
		array = oneline.strip().split("\t")
		rsIDTemp.append(array[0])
	
	IndSNPList = select_Indipendent_snp(rsIDTemp,0.8)
	get_candidate_variants(IndSNPList,0.95,'CHB')

	outfile.close()

if __name__ == "__main__":
	sys.exit(main())