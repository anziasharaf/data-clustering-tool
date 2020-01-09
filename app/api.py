from __future__ import print_function
import sys
import zerorpc
import shutil
import csv
import pandas
import ezodf
import hashing
import os
import process_data
import ml2en

def get_mulList(*args):
    return map(list,zip(*args))

class CalcApi(object):
	def echo(self, text):
		try:
			for the_file in os.listdir("Output"):
				file_path = os.path.join("Output", the_file)
				if os.path.isfile(file_path):
					os.unlink(file_path)
			file=text
			namecom = file.split("/")[-1].split(".")
			name = namecom[0]
			filetype = namecom[-1]
			first_record_key = []
			if filetype == "xlsx":
				xl = pandas.read_excel(file)
				xl.to_csv(name + '.csv', encoding='utf-8')
				total_dict = xl.to_dict()
				first_record_key = list(total_dict.keys())
			elif filetype == "xls":
				xl = pandas.read_excel(file)
				xl.to_csv(name + '.csv', encoding='utf-8')
				total_dict = xl.to_dict()
				first_record_key = list(total_dict.keys())
			elif filetype == "ods":
				doc = ezodf.opendoc(file)
				sheet = doc.sheets[0]
				df_dict = {}
				for i, row in enumerate(sheet.rows()):
					if i == 0:
						df_dict = {cell.value:[] for cell in row}
						col_index = {j:cell.value for j, cell in enumerate(row)}
						continue
					for j, cell in enumerate(row):
						df_dict[col_index[j]].append(cell.value)
				myFile = open(name + '.csv', 'w')
				total_dict = df_dict
				total_dict_keys = list(total_dict.keys())
				first_record_key = total_dict_keys[0]
				total_number_of_records = len(total_dict[first_record_key])
				first_record_key = total_dict_keys
				with myFile:
					writer = csv.writer(myFile)
					writer.writerows([['']+total_dict_keys])
					for i in range(total_number_of_records):
						array = []
						for nam in total_dict_keys:
							array.append(total_dict[nam][i])
						writer.writerows([[i]+array])
						
			elif filetype == "csv":
				shutil.copy(file, os.getcwd())
				with open(file, newline='') as f:
					reader = csv.reader(f)
					first_record_key = next(reader)
			return [sorted(first_record_key),name]
		except Exception as e:
			return e

	def submit(self, list_data):
		try:
			threshhold = list_data[0]
			hash_data = list_data[1]
			trans = list_data[2]
			ml2eng = ml2en.ml2en() 
			myfile = open('bucket.csv','w')
			dbs = list(hash_data.keys())
			with myfile:
				writer = csv.writer(myfile)
				writer.writerows([["ID","Data"]])
				for db in dbs:
					array1 = []
					array2 = []
					schema_hash = hash_data[db]
					csv_data = open(db+'.csv','r')
					data = list(csv.reader(csv_data))
					ind_dict = dict(zip(data[0],get_mulList(*data[1:])))
					for schema in schema_hash:
						if array2 == []:
							array1 = ind_dict[schema]
						else:
							array2 = ind_dict[schema]
							array1 = list(map(''.join, zip(array1, array2)))
						array1 = [ a + ' ' for a in array1]
						array2 = ind_dict[schema]
					for i in range(len(array1)):
						main_data = array1[i]
						if trans == "true":
							main_data = ml2eng.transliterate(array1[i])
						writer.writerows([[db+"|"+str(i),main_data]])
			total = hashing.hashing(threshhold,'bucket.csv',trans)
			tot = process_data.begin_execute()
			return tot

		except Exception as e:
			return e
	
	def get_data(self, string):
		try:
			process_data.begin_execute()
			return_value = process_data.call_the_next_or_previous_record(string)
			return return_value		
		except Exception as e:
			return e

	def delete_record(self, record_data):
		try:
			id_rec = record_data[0]
			db = record_data[1]
			deletion = record_data[2]
			xl = pandas.read_csv("Output/"+db+".csv")
			if deletion=="DELETE":
				xl["Sched_for_deletion"][int(id_rec)] = "DELETE"
			else:
				xl["Sched_for_deletion"][int(id_rec)] = ""
			#xl.drop(int(id_rec), inplace=True)
			xl.to_csv("Output/"+db+".csv", encoding='utf-8', index=False)
			return "success"		
		except Exception as e:
			return e

	def execute(self, text):
		try:
			for the_file in os.listdir("Output"):
				xl = pandas.read_csv("Output/"+the_file)
				indexes_to_drop = []
				for j in range(xl.shape[0]):
					if xl["Sched_for_deletion"][j] == "DELETE":
						indexes_to_drop.append(j)			
				xl.drop(xl.index[indexes_to_drop], inplace=True)
				xl.drop('Sched_for_deletion', axis=1, inplace=True)
				xl.drop('Similarities', axis=1, inplace=True)
				xl.to_csv("Output/"+the_file, encoding='utf-8', index=False)
			print(text)
			os.system("rm *.csv")
			return "success"
		except Exception as e:
			return e		

def parse_port():
	port = 4242
	try:
		port = int(sys.argv[1])
	except Exception as e:
		pass
	return '{}'.format(port)

def main():
	addr = 'tcp://127.0.0.1:' + parse_port()
	s = zerorpc.Server(CalcApi())
	s.bind(addr)
	print('start running on {}'.format(addr))
	s.run()

if __name__ == '__main__':
	main()
