import numpy as np
import helper
import collect
import convert

mos = np.arange(1, 13)
yrs = np.arange(11, 19)

dates = {}

for y in yrs:
    dates['20' + str(y)] = []
    for m in mos:
        dates['20' + str(y)].append(helper.make_dates(str(m), '20' + str(y)))

str_yrs = [date for date in dates]

a_year = input("Enter a year:")

collect.search_dates(dates, a_year)

