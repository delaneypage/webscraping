import numpy as np
import helper
import collect
import convert

start_yr = input("Enter a year: ")
start_mo = input("Enter a starting month: ")
end_mo = input("Enter an ending month: ")

dates = {}

yrs = [int(start_yr)]
mos = np.arange(int(start_mo), int(end_mo))

for y in yrs:
    dates['20' + str(y)] = []
    for m in mos:
        dates['20' + str(y)].append(helper.make_dates(str(m), '20' + str(y)))

str_yrs = [date for date in dates]

collect.search_dates(dates)

