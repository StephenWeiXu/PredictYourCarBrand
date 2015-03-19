
# Compute the results after manually check

import os
import csv
import numpy as np
import re


result_1_2000 = np.genfromtxt("1_2000.csv", delimiter=';', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_1_2000)
result_2001_3000 = np.genfromtxt("2001_3000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_2001_3000)
result_3001_4000 = np.genfromtxt("3001_4000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_3001_4000)
result_4001_5000 = np.genfromtxt("4001_5000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_4001_5000)
result_1_2000, result_2001_3000,result_3001_4000, result_4001_5000 = list(result_1_2000), list(result_2001_3000), list(result_3001_4000), list(result_4001_5000)

result_1_2000.extend(result_2001_3000)
result_1_2000.extend(result_3001_4000)
result_1_2000.extend(result_4001_5000)
#print result_1_2000

user_id = []
car_label = []
tweet = []
with open('tweet_data_all_5000.csv', 'r') as f:
    r = csv.reader(f, delimiter = '|')
    for row in r:
    	user_id.append(row[0])
    	car_label.append(row[1])
    	tweet.append(row[2])
    	#print row[0], row[1]

#print len(user_id)
#print len(car_label)
#print len(result_1_2000)

valid_user_id = []
valid_car_label = []
for ind in range(0, len(result_1_2000)):
	row = result_1_2000[ind]
	if row[1] == "T" and not re.match('rt', tweet[row[0] -1]):
		valid_car_label.append(car_label[row[0]-1])
		valid_user_id.append(user_id[row[0]-1])

print len(valid_user_id)
print len(valid_car_label)

brand_list = list(set(valid_car_label))
for brand in brand_list:
	print brand, valid_car_label.count(brand)

