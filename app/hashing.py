from datasketch import MinHash, MinHashLSH
from nltk import ngrams
import csv
import pandas as pd
import sys


def hashing(threshold_val,loaded_file,trans):
	data = []
	with open(loaded_file, 'rU') as infile:
		reader = csv.DictReader(infile)
		for row in reader:
			#print(row['Data'].lower())
			main_data = row['Data'].lower().replace(' ','').replace('.','').replace(',','')
			data.append(main_data)

	# Create an MinHashLSH index optimized for Jaccard threshold 0.5,
	# that accepts MinHash objects with 128 permutations functions
	lsh = MinHashLSH(threshold=float(threshold_val), num_perm=256)

	# Create MinHash objects
	minhashes = {}
	for c, i in enumerate(data):
	  minhash = MinHash(num_perm=256)
	  for d in ngrams(i, 3):
	    minhash.update("".join(d).encode('utf-8'))
	  lsh.insert(c, minhash)
	  minhashes[c] = minhash

	random_hash = {}
	random_hash_2 = {}
	random_hash["Similarities"] = [] 
	for i in range(len(minhashes.keys())):
		result = lsh.query(minhashes[i])
		random_hash["Similarities"].append(result)

	del lsh
	del minhashes
	csv_input = pd.read_csv(loaded_file)
	csv_input['Similarities'] = random_hash["Similarities"]
	csv_input.to_csv('output.csv', index=False)



	with open('output.csv', 'rU') as infile:
		reader = csv.DictReader(infile)
		lock = ''
		myfile = ''
		row_no = 1
		row_array = {}
		row_array["Similarities"] = []
		row_array['Sched_for_deletion'] = []
		num = 0
		for row in reader:
			record = row["ID"].split("|")
			filename = record[0]
			if lock == filename:
				results = row["Similarities"][1:-1].split(",")
				array = []
				for r in results:
					array.append(csv_input.iloc[int(r),0])
				if len(array) > 1:
					num = num + 1
					row_array["Similarities"].append(array)
				else:
					row_array["Similarities"].append("")
				row_array['Sched_for_deletion'].append("")
			else:
				if lock != '':
					myfile['Similarities'] = row_array["Similarities"]
					myfile['Sched_for_deletion'] = row_array['Sched_for_deletion']
					myfile.to_csv('Output/'+lock+'.csv', index=False)
				myfile = pd.read_csv(filename+'.csv')
				lock = filename
				row_array["Similarities"] = []
				row_array['Sched_for_deletion'] = []
				results = row["Similarities"][1:-1].split(",")
				array = []
				for r in results:
					array.append(csv_input.iloc[int(r),0])
				if len(array) > 1:
					num = num + 1
					row_array["Similarities"].append(array)
				else:
					row_array["Similarities"].append("")
				row_array['Sched_for_deletion'].append("")
		myfile['Similarities'] = row_array["Similarities"]
		myfile['Sched_for_deletion'] = row_array['Sched_for_deletion']
		myfile.to_csv('Output/'+lock+'.csv', index=False)
	return num
