def make_dates(month, year):
    if int(month) == 9:

        date1 = '0' + month + '/' + '01' + '/' + year
        date2 = '0' + month + '/' + '15' + '/' + year
        date3 = '10' + '/' + '01' + '/' + year

    elif int(month) > 9:

        date1 = month + '/' + '01' + '/' + year
        date2 = month + '/' + '15' + '/' + year

        if int(month) == 12:

            year = str(int(year) + 1)
            date3 = '01' + '/' + '01' + '/' + year

        else:

            month = str(int(month) + 1)
            date3 = month + '/' + '01' + '/' + year

    else:

        date1 = '0' + month + '/' + '01' + '/' + year
        date2 = '0' + month + '/' + '15' + '/' + year
        month = str(int(month) + 1)
        date3 = '0' + month + '/' + '01' + '/' + year

    return [date1, date2, date3]

