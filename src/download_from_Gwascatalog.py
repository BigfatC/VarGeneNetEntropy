#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: download_from_Gwascatalog.py
@time: 18-10-10 2:08
"""

import json
import requests, sys, re

EFONAME = sys.argv[1]
OutPath = sys.argv[2]

OutFile = open(OutPath,'a+')

# get association studies with REST API
def get_with_traits(EFO_id,P_upper,query_num,start,maf):
	# output define
	#outputname = EFO_id + "_gwas_catalog.txt"
	#outputpath = '/Users/caiyiran/Downloads/Dissertation/scripts/' + outputname
	#output = open(outputpath,'a+')
	# signal requests
	server = "https://www.ebi.ac.uk/gwas/summary-statistics/api/traits/"+ EFO_id \
		+ "/associations"+ "?size=" + str(query_num)+ "&p_upper=" + P_upper + "&start=" + str(start)
	r = requests.get(server,headers={"Content-Type" : "application/json"})
	if not r.ok:
		return 0
		r.raise_for_status()
		sys.exit()
		
	decoded = r.content.decode()
	dict_decoded = json.loads(decoded)
	associations = dict_decoded['_embedded']['associations']

	if len(associations):
		len_dict = len(associations)
		if start == 0:
			print("rsID\tchr\tloc\tp_value\tbeta\tOR\tci_upper\tci_lower\tallele_freq\tref\talt\tstudycession"
				,file = OutFile)
		for j in range(len_dict): #for display we only allow 10 queries
			i = str(j)
			beta = associations[i]['beta']
			ci_upper = associations[i]['ci_upper']
			chromosome = associations[i]['chromosome']
			study_accession = associations[i]['study_accession']
			other_allele = associations[i]['other_allele']
			base_pair_location = associations[i]['base_pair_location']
			odds_ratio = associations[i]['odds_ratio']
			ci_lower = associations[i]['ci_lower']
			variant_id = associations[i]['variant_id']
			p_value = associations[i]['p_value']
			effect_allele = associations[i]['effect_allele']
			effect_allele_frequency = associations[i]['effect_allele_frequency']
			if odds_ratio: #and effect_allele_frequency and effect_allele_frequency >= maf:
				if odds_ratio > 1.0 and ci_lower > 1.0:
					print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}".\
						format(variant_id,chromosome,base_pair_location,p_value,beta,odds_ratio,ci_upper,\
							   ci_lower,effect_allele_frequency,other_allele,\
								effect_allele,study_accession),file = OutFile)
	else:
		print("No Associations Found.")     
	return 1

def main():
	start = 0
	each_query = 100
	maximum = 3000
	while get_with_traits('EFO_0002690','5E-8',each_query,start,0.01):
		start += each_query
		if start >= maximum:
			break
		#print(start)

	OutFile.close()



if __name__ == "__main__":
	sys.exit(main())