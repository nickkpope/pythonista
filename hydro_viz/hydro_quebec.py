import csv
import appex

import collections
import datetime


def control_for_hourly_temp(kwh, temp):
	normalized_temp = (temp - min_hourly_temp)/(max_hourly_temp - min_hourly_temp)
	return kwh * normalized_temp


def control_for_daily_temp(kwh, temp):
	normalized_temp = (temp - min_daily_temp)/(max_daily_temp - min_daily_temp)
	return kwh * normalized_temp


def to_cad(kwh):
	''' Converts from Kilowatt hours to Candian dollars. 
	'''
	return kwh*252.56/2829


def csv_reader(filename):
	if appex.is_running_extension():
		file_path = appex.get_text()
	else:
		file_path = filename
		
	stream = open(file_path, 'rb').read().decode('utf-8').split('\n')
	return iter(csv.reader(stream, delimiter=';'))
	

def kwh_by_day():
	
	reader = csv_reader('daily_usage.csv')
	headers = reader.__next__()
	data = []
	
	for line in reader:
		if not line:
			continue
		kwh = float(line[3]) if line[3] else 0.0
		yield datetime.datetime.strptime(line[2], '%Y-%m-%d'), kwh, control_for_daily_temp(kwh, int(line[5]))


def temp_by_day():
	reader = csv_reader('daily_usage.csv')
	headers = reader.__next__()
	
	for line in reader:
		if not line:
			continue

		yield int(line[5])


def temp_by_hour():
	reader = csv_reader('hourly_usage.csv')
	headers = reader.__next__()
	
	for line in reader:
		if not line:
			continue

		yield int(line[4])

def kwh_by_hour():
	reader = csv_reader('hourly_usage.csv')
	headers = reader.__next__()
	
	for line in reader:
		if not line:
			continue
		
		kwh = float(line[2]) if line[2] else 0.0
		# 2017-12-18 20:00:00
		yield datetime.datetime.strptime(line[1], '%Y-%m-%d %H:%M:%S'), control_for_hourly_temp(kwh, int(line[4]))


def avg_kwh_by_hour_of_day():
	bucket = collections.defaultdict(
		lambda: collections.defaultdict(list))
	for time_of_day, kwh in kwh_by_hour():
		td = time_of_day.hour+\
			time_of_day.minute/60+\
			time_of_day.second/120
		day_of_the_week = time_of_day.weekday()
		bucket[day_of_the_week][td].append(kwh)

	ret = collections.defaultdict(dict)
	for dofw, ds in bucket.items():
		for td, kwhs in ds.items():
			ret[dofw][td] = float(sum(kwhs))/len(kwhs)

	return ret

hourly_temps = list(temp_by_hour())
min_hourly_temp = min(hourly_temps)
max_hourly_temp = max(hourly_temps)

daily_temps = list(temp_by_day())
min_daily_temp = min(daily_temps)
max_daily_temp = max(daily_temps)
