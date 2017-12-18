import matplotlib.pyplot as plt

import hydro_quebec


dates, kwhs = zip(*hydro_quebec.kwh_per_day())

plt.subplot(2, 1, 1)
plt.plot(dates, kwhs)
plt.title('Kilowatts per day.')
#plt.xlabel('Day')
plt.ylabel('Energy (kwh)')

plt.subplot(2, 1, 2)
plt.plot(dates, [hydro_quebec.to_cad(item) for item in kwhs], 'r.-')
plt.title('Cost per day.')
plt.xlabel('Day')
plt.ylabel('Cost (CAD)')

plt.show()

