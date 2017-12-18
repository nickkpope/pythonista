import csv
import appex
from datetime import datetime

def to_cad(kwh):
	''' Converts from Kilowatt hours to Candian dollars. 
	'''
	return kwh*252.56/2829


def kwh_per_day():
	if appex.is_running_extension():
		file_path = appex.get_text()
	else:
		file_path = 'raw_data.csv'
		
	stream = open(file_path, 'rb').read().decode('utf-8').split('\n')
	reader = iter(csv.reader(stream, delimiter=';'))
	
	headers = reader.__next__()
	data = []
	
	for line in reader:
		if not line:
			continue
		yield(datetime.strptime(line[2], '%Y-%m-%d'), float(line[3]))

