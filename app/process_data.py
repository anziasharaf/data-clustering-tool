import os
import sys
import csv
import time
import pandas as pd

global begin
begin = 0
global unique_list
unique_list=[]
def call_the_next_or_previous_record(n_or_p):
	if n_or_p == "n":
		k = begin
		global begin
		begin = k+1
	elif n_or_p == "start":
		global begin
		begin = 0
	else:
		k = begin
		global begin
		if k != 0:
			begin = k-1
		else:
			begin = 0
	return 	take_the_record(unique_list[begin])

def take_the_record(arr):
	records = []
	arr = arr.split(",")
	for x in arr:
		t = {}
		i= int(x)
		trig = pd.read_csv("output.csv")
		db_record_string = trig["ID"][i].split("|")
		db=db_record_string[0]
		row_num = db_record_string[1]
		data_b = pd.read_csv(db+".csv")
		real_data_b = pd.read_csv("Output/"+db+".csv")
		locate_record = data_b.iloc[[int(row_num)]]
		dict_locate = locate_record.to_dict()
		dict_locate["icfoss_database"] = db
		dict_locate["icfoss_deleted?"] = real_data_b["Sched_for_deletion"][int(row_num)]
		records.append(dict_locate)
	return records

def begin_execute():
	f = open("output.csv", "r")
	reader = csv.reader(f)
	bucket_list = []
	for row in reader:
		string = row[-1][1:-1]
		multiple = string.split(",")
		if len(multiple) > 1:
			bucket_list.append(string)
	f.close()
	global unique_list
	unique_list = list(set(bucket_list))
	return len(unique_list)


