import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from practice6.plots import *

data_list = []
data1 = pd.DataFrame()
data1_cols = ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
			"v_homeruns", "v_rbi"]

for chunk in pd.read_csv("data/[1]game_logs.csv", chunksize=10000,
						 usecols=data1_cols, low_memory=False, index_col=False):
	data1 = pd.concat([data1, chunk], ignore_index=True)
data_list.append(data1)

data2 = pd.DataFrame()
data2_cols = ["FLIGHT_NUMBER", "ORIGIN_AIRPORT", "DAY_OF_WEEK", "DESTINATION_AIRPORT", "DISTANCE", "AIR_TIME",
			"TAXI_OUT", "ARRIVAL_DELAY",
			"AIRLINE", "TAXI_IN"]
for chunk in pd.read_csv("data/[3]flights.csv", chunksize=10000,
						 usecols=data2_cols, low_memory=False, index_col=False):
	data2 = pd.concat([data2, chunk], ignore_index=True)
data_list.append(data2)

data3 = pd.DataFrame()
data3_cols = ["vf_Make", "stockNum", "vf_EngineCylinders", "vf_EngineKW", "vf_EngineModel", "vf_EntertainmentSystem",
			"vf_ForwardCollisionWarning", "vf_FuelInjectionType",
			"vf_FuelTypePrimary", "vf_FuelTypeSecondary"]
for chunk in pd.read_csv("data/[2]automotive.csv.zip", compression='zip', chunksize=10000,
						 usecols=data3_cols, low_memory=False, index_col=False):
	data3 = pd.concat([data3, chunk], ignore_index=True)
data_list.append(data3)

data4 = pd.DataFrame()
data4_cols = ["name", "spkid", "class", "diameter", "albedo", "diameter_sigma",
			"epoch", "epoch_cal",
			"om", "w"]
for chunk in pd.read_csv("data/[5]asteroid.zip", compression='zip', chunksize=10000,
						 usecols=data4_cols, low_memory=False, index_col=False):
	data4 = pd.concat([data4, chunk], ignore_index=True)
data_list.append(data4)

data5 = pd.DataFrame()
data5_cols = ["id", "key_skills", "schedule_name", "experience_id", "experience_name", "salary_from",
			"salary_to", "employer_name",
			"employer_industries", "schedule_id"]
for chunk in pd.read_csv("data/[4]vacancies.csv.gz", compression='gzip', chunksize=10000,
						 usecols=data5_cols, low_memory=False, index_col=False):
	data5 = pd.concat([data5, chunk], ignore_index=True)
data_list.append(data5)



def analyze_data(source_dataframe: pd.DataFrame):
	file_size = source_dataframe.memory_usage(deep=True).sum()
	memory_usage = source_dataframe.memory_usage(deep=True).sum()
	col_sizes = []
	for col in source_dataframe.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		col_sizes.append({'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	source_data = source_dataframe.loc[:, source_dataframe.dtypes != object]
	sorted_sizes = []
	for col in source_data.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		sorted_sizes.append(
			{'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


result_analyze = []
for data in data_list:
	result_analyze.append(analyze_data(data))

with open("results.json", 'a') as file:
	for index, data in enumerate(result_analyze):
		json.dump({f'data{index}_memory_usage': data['col_sizes']}, file)


def convert_data(data):
	converted_data = data.copy()
	for column in converted_data.columns:
		if converted_data[column].dtype == 'object':
			unique_values = converted_data[column].unique()
			if len(unique_values) < 50:
				converted_data[column] = converted_data[column].astype('category')
			if converted_data[column].dtype == 'int64':
				converted_data[column] = converted_data[column].astype(np.int32)
			elif converted_data[column].dtype == 'float64':
				converted_data[column] = converted_data[column].astype(np.float32)
	return converted_data


def analyze_optimized_data(data):
	return convert_data(data)


def compare_memory_usage(source_data, optimized_data):
	source_data_memory = source_data.memory_usage(deep=True).sum()
	optimized_data_memory = optimized_data.memory_usage(deep=True).sum()
	if source_data_memory > optimized_data_memory:
		print("optimized data lighter than source data on - " + str(
			source_data_memory - optimized_data_memory))
	else:
		print("optimized data heavier than source data on - - " + str(
			optimized_data_memory - source_data_memory))
		
for index, data in enumerate(data_list):
	optimized_data = analyze_optimized_data(data)
	compare_memory_usage(data, optimized_data)
	optimized_data.to_csv(f'optimized_data_{index + 1}.csv')


#CREATE PLOTS
linear(data1, "v_score", "h_score", "1_1")
linear(data1, "v_hits", "v_doubles", "1_2")
linear(data1, "v_hits", "v_triples", "1_3")
stepped(data1, "v_homeruns", "v_hits", "1_4")
stepped(data1, "v_homeruns", "v_score", "1_5")
linear(data2, "DISTANCE", "AIR_TIME", "2_1")
linear(data2, "FLIGHT_NUMBER", "TAXI_IN", "2_2")
histogram(data2, "DISTANCE", "TAXI_OUT", "2_3")
histogram(data2, "FLIGHT_NUMBER", "TAXI_OUT", "2_4")
histogram(data2, "FLIGHT_NUMBER", "AIR_TIME", "2_5")
linear(data3, "vf_ForwardCollisionWarning", "vf_EngineCylinders", "3_1")
linear(data3, "vf_EngineCylinders", "vf_FuelTypePrimary", "3_2")
stepped(data3, "vf_EngineKW", "vf_FuelTypeSecondary", "3_3")
linear(data3, "vf_EngineCylinders", "vf_FuelTypeSecondary", "3_4")
histogram(data3, "vf_EngineCylinders", "vf_EngineKW", "3_5")
linear(data4, "class", "diameter", "4_1")
stepped(data4, "spkid", "class", "4_2")
histogram(data4, "spkid", "diameter", "4_3")
box(data4, "class", "albedo", "4_4")
histogram(data4, "diameter", "diameter_sigma", "4_5")
linear(data5, "id", "salary_to", "5_1")
linear(data5, "id", "salary_from", "5_2")
stepped(data5, "schedule_id", "experience_id", "5_3")
box(data5, "experience_id", "salary_to", "5_4")
histogram(data5, "experience_id", "salary_from", "5_5")