
''' Data Preprocessing Functions
Please write your data preocessing method here, including PCA, SMOTE, CMU Research etc '''

import sys
import numpy as np

''' Print the statistics of the car brand label '''
def printStats(label):
	car_brands = {0:'bmw', 1:'honda', 2:'jeep', 3:'audi', 4:'ford', 5:'hyundai', 6:'kia', 7:'lexus', 8:'mazda', 9:'nissan', 10:'toyota', 11:'ferrari'}

	label = list(label)
	label_unique = list(set(label))
	for item in label_unique:
		print item, car_brands[item],label.count(item)



