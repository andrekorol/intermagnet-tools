from urlget import download_from_url
import os
import zipfile
import shutil
import gzip
import math
import numpy as np
import matplotlib.pyplot as plt


if not os.path.isdir("data"):
    os.makedirs("data")

download_from_url("https://raw.githubusercontent.com/andrekorol/intermagnet-to\
ols/master/quietest.zip",
                  "data")

zip_ref = zipfile.ZipFile("data/quietest.zip", 'r')
zip_ref.extractall("data")
zip_ref.close()

quietest_days = [5, 9, 20, 21, 28]

H_dict = {}

for root, dirs, files in os.walk("data"):
    for file in files:
        ext = file.split('.')[-1]
        if ext == 'gz':
            with gzip.open(os.path.join(root, file), 'rb') as fin:
                for line in fin:
                    decoded_line = line.decode("utf-8")
                    if decoded_line[0] != ' ' and decoded_line[0] != 'D':
                        values = decoded_line.split()
                        #  print(values)
                        date = values[0]
                        x = float(values[3])
                        y = float(values[4])
                        day = date.split('-')[-1]
                        if day not in H_dict:
                            H_dict[day] = [math.sqrt(x ** 2 + y ** 2)]
                        else:
                            H_dict[day].append(math.sqrt(x ** 2 + y ** 2))

H_5_6_arr = np.array(H_dict['05'][180:] + H_dict['06'][:180])
H_9_10_arr = np.array(H_dict['09'][180:] + H_dict['10'][:180])
H_20_21_arr = np.array(H_dict['20'][180:] + H_dict['21'][:180])
H_21_22_arr = np.array(H_dict['21'][180:] + H_dict['22'][:180])
H_28_1_arr = np.array(H_dict['28'][180:] + H_dict['01'][:180])
max_idx = H_28_1_arr.argmax(axis=0)
substitute = (H_28_1_arr[max_idx - 1] + H_28_1_arr[max_idx + 1]) / 2
print(substitute)
H_28_1_arr[max_idx] = substitute
quietest_days_list = [H_5_6_arr, H_9_10_arr, H_20_21_arr, H_21_22_arr,
                      H_28_1_arr]

H_27_28_arr = np.array(H_dict['27'][180:] + H_dict['28'][:180])

mean_H_arr = np.mean([H_5_6_arr, H_9_10_arr, H_20_21_arr, H_21_22_arr,
                     H_28_1_arr], axis=0)
delta_H = np.subtract(H_27_28_arr, mean_H_arr)

time_axis_arr = np.array([i for i in range(1440)])

plt.plot(time_axis_arr, H_27_28_arr, label='27')
plt.plot(time_axis_arr, H_5_6_arr, label='5')
plt.plot(time_axis_arr, H_9_10_arr, label='9')
plt.plot(time_axis_arr, H_20_21_arr, label='20')
plt.plot(time_axis_arr, H_21_22_arr, label='21')
plt.plot(time_axis_arr, H_28_1_arr, label='28')
plt.plot(time_axis_arr, mean_H_arr, label='media')
plt.legend()
#  for day in quietest_days_list:
#      plt.plot(time_axis_arr, day)
plt.show()
plt.savefig("havg.png")

shutil.rmtree("data")
