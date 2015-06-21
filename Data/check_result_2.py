
# Compute the results after manually check

import os
import csv
import numpy as np
import re

''' Open the dataset after manually check'''
result_1_2000 = np.genfromtxt("1_2000.csv", delimiter=';', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_1_2000)
result_2001_3000 = np.genfromtxt("2001_3000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_2001_3000)
result_3001_4000 = np.genfromtxt("3001_4000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_3001_4000)
result_4001_5000 = np.genfromtxt("4001_5000.csv", delimiter=',', dtype = [('myint', 'i8'), ('mystring', 'S5')])
#print len(result_4001_5000)
result_1_2000, result_2001_3000,result_3001_4000, result_4001_5000 = list(result_1_2000), list(result_2001_3000), list(result_3001_4000), list(result_4001_5000)

''' Combine all 5000 users' id and corresponding car label '''
result_1_2000.extend(result_2001_3000)
result_1_2000.extend(result_3001_4000)
result_1_2000.extend(result_4001_5000)
#print result_1_2000

''' Match and get valid user '''
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
	if row[1] == "T" and not re.match('rt', tweet[row[0]-1]):
		valid_car_label.append(car_label[row[0]-1])
		valid_user_id.append(user_id[row[0]-1])

#print len(valid_user_id)
#print len(valid_car_label)

''' Get unique valid users '''
unique_user_id = []
unqiue_car_label = []
for i in range(0, len(valid_user_id)):
    if valid_user_id[i] in unique_user_id:
        continue
    unique_user_id.append(valid_user_id[i])
    unqiue_car_label.append(valid_car_label[i])

#print len(unique_user_id)
#print len(unqiue_car_label)

''' Compute the statistics of the final valid results'''

brand_list = list(set(unqiue_car_label))
for brand in brand_list:
	print brand, unqiue_car_label.count(brand)

''' unique_user_id contains all unqiue and valid user_id, which can be used to retirve their more tweets. 
    unqiue_car_label contains ther corresponding car brand '''
all_valid_info = []
for ind in range(0, len(unique_user_id)):
    all_valid_info.append([unique_user_id[ind], unqiue_car_label[ind]])

print len(all_valid_info) 
'''
with open("valid_user_label.csv", 'w') as fp:
    csv_writer = csv.writer(fp, delimiter = ',')
    for item in all_valid_info:
        csv_writer.writerow(item)
'''