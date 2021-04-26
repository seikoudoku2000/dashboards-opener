import csv
import argparse
import datetime
import sys
import webbrowser


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='This script will open dashboards in the list with the timestamp passed as parameter') 

	parser.add_argument('timestamp', type=int, help='central timestamp you want to check in milliseconds epoch format.')
	parser.add_argument('--duration', type=int, default=30, help='time range you want to check before and after the central timestamp(minute). default: 10')
	parser.add_argument('--file', type=str, default='base_urls.csv', help='csv file where dashboard urls are defined. default: base_urls.csv')

	args = parser.parse_args()
	target_timestamp = args.timestamp
	dashboard_duration = args.duration
	urls_csv_file = args.file
	# print('target_timestamp: ' + str(target_timestamp))
	# print('duration: ' + str(dashboard_duration))
	incident_timestamp = target_timestamp
	incident_date = datetime.datetime.fromtimestamp(incident_timestamp / 1000)

	start_date = incident_date - datetime.timedelta(minutes=dashboard_duration)
	start_timestamp = str(int(start_date.timestamp() * 1000))
	end_date = incident_date + datetime.timedelta(minutes=dashboard_duration)
	end_timestamp = str(int(end_date.timestamp() * 1000))

	csv_file = open(urls_csv_file, "r")
	f = csv.reader(csv_file, delimiter=",", doublequote=True, quotechar='"', skipinitialspace=True)
	header = next(f)
	for row in f:
		base_url = row[0]
		if base_url.startswith("#"):
			continue
		# print(base_url)
		target_url = base_url.replace('START_TIMESTAMP', start_timestamp).replace('END_TIMESTAMP', end_timestamp)
		# print(target_url)
		webbrowser.open(target_url)
