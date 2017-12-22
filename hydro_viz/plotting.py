import matplotlib.pyplot as plt
import console

import hydro_quebec

dofw_labels = [
	'Monday',
	'Tuesday',
	'Wednesday',
	'Thursday',
	'Friday',
	'Saturday',
	'Sunday',
]


def plot_kwhs_per_day():

	dates, kwhs, ckwhs = zip(*hydro_quebec.kwh_by_day())

	ax = plt.subplot(2, 1, 1)
	plt.plot(dates, kwhs, label='kwh')
	plt.plot(dates, ckwhs, label='controlled')
	
	plt.title('Kilowatts per day.')
	#plt.xlabel('Day')
	plt.ylabel('Usage')
	ax.legend(bbox_to_anchor=(0.3, 1.2))

	plt.subplot(2, 1, 2)
	plt.plot(dates, [hydro_quebec.to_cad(item) for item in kwhs], 'r.-')
	plt.title('Cost per day.')
	plt.xlabel('Day')
	plt.ylabel('Cost (CAD)')
	
	plt.show()
	
	
def plot_daily_usage():
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	
	# need to sum the kwhs for each hour of the day
	for dofw, adu in hydro_quebec.avg_kwh_by_hour_of_day().items():
		x, y = zip(*adu.items())

		ret=plt.plot(x, y, label=dofw_labels[dofw])

	plt.legend(bbox_to_anchor=(1.2, 1))
	plt.xlabel('Time of Day')
	plt.ylabel('Usage (controlled)')
	plt.title('Usage throughout the day.')
	
	plt.show()

plot_map = {
	1: plot_kwhs_per_day,
	2: plot_daily_usage,
}
plot_map[console.alert(
	'Views',
	'Choise which plot you would like to see.',
	'Kwh per day',
	'Daily usage',
)]()
	

