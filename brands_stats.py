import csv
import operator
brand_counts = {}
total = 0.0
with open('tweet_data_partial.csv', 'r') as f:
    r = csv.reader(f, delimiter = '|')
    for row in r:
        total = total + 1
        brand = row[1]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

l = sorted(brand_counts.items(), key = operator.itemgetter(1), reverse = True)

for x in l:
    print x[0] + ' %2.2f' %(x[1]/total)