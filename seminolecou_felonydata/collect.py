from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support import expected_conditions as ec
import jsonlines
import time
import re


def search_dates(date_ranges, year=0):

    """
    :param date_ranges: dictionary { 'string' : list [ of dates ] }
    :param year: year of collection
    :return:
    """

    url = 'https://courtrecords.seminoleclerk.org/criminal/'
    chromedriver = "/Applications/chromedriver"

    try:
        print("making driver", end='')
        print(".", end='')
        driver = webdriver.Chrome(chromedriver)
        print(".", end='')
        driver.get(url)
        print(".", end='')

    except SessionNotCreatedException:
        print("... ERROR: driver failed")

    print("driver initialized")

    check = driver.find_element_by_xpath('//*[@id="MainContent_MM_Cat"]')
    check.click()

    def search_from(_from, _to):

        from_date = driver.find_element_by_xpath('//*[@id="fromDateTxt"]')
        from_date.clear()
        from_date.send_keys(_from)

        to_date = driver.find_element_by_xpath('//*[@id="toDateTxt"]')
        to_date.clear()
        to_date.send_keys(_to)

        search = driver.find_element_by_xpath('//*[@id="search"]')
        search.click()

        wait = WebDriverWait(driver, 10)

        driver.implicitly_wait(10)

        table = driver.find_element_by_id('CaseGrid')
        rows = table.find_elements_by_tag_name('tr')[1:]

        records = len(rows)
        count = 1

        for row in rows:

            rdata = row.find_elements_by_tag_name('td')

            case_num = rdata[0]
            case_name = rdata[1]

            #case_num.get_attribute('id')

            if case_name.text.find('CONFIDENTIAL') == -1:

                case_num.click()

                collect_data(rdata, driver)

                print(' record: ', str(count) + '/' + str(records))
                count += 1

                #     case_num.click()
                #
                #     collect_data(rdata, driver)
                #     print(' record: ', str(count) + '/' + str(records))
                #     count += 1


        return True

        # original search

        # table = driver.find_element_by_id('CaseGrid')
        # rows = table.find_elements_by_tag_name('tr')[1:]

    if int(year) > 0:

        yr = '20' + str(year)

        for date_range in date_ranges[yr]:

            the_1st, the_15th, next_1st = date_range[0], date_range[1], date_range[2]

            search_from(the_1st, the_15th)
            search_from(the_15th, next_1st)

        return True

    elif int(year) == 0:

        for i in date_ranges:

            date_range = date_ranges[i][0]

            the_1st, the_15th, next_1st = date_range[0], date_range[1], date_range[2]

            if search_from(the_1st, the_15th):
                search_from(the_15th, next_1st)

        return True


def collect_data(row, d):

    case = row[0].text
    name = row[1].text
    due = row[8].text

    wait = WebDriverWait(d, 10)

    category = row[2].find_element_by_id('category').get_attribute('title')
    status = row[7].find_element_by_id('status').get_attribute('title')

    d.switch_to.window(d.window_handles[1])

    time.sleep(1)

    party_info = wait.until(ec.element_to_be_clickable((by.XPATH, '//*[@id="party_pan"]')))
    charge_details = wait.until(ec.element_to_be_clickable((by.XPATH, '//*[@id="chrg_pan"]')))

    # except NoSuchElementException:
    #
    #     d.close()
    #     d.switch_to.window(d.window_handles[0])
    #     return False

    party_info.click()

    time.sleep(1)

    charge_details.click()

    ucn = d.find_element_by_id('MainContent_UCN').text
    arrest_rpt = d.find_element_by_id('MainContent_arrestRptNumber').text
    arrest_date = d.find_element_by_id('MainContent_arrestDate').text
    close_date = d.find_element_by_id('MainContent_closeDate').text

    temp_table = wait.until(ec.presence_of_element_located((by.XPATH, '//*[@id="lbl_partyDemogr"]/table'))
                            ).text.split('\n')

    dem_table = {}
    words = ['DL', 'Color', 'Height']

    for val in temp_table:
        key_and_val = val.split(':')
        if not any(i in key_and_val[0] for i in words):
            dem_table[key_and_val[0]] = key_and_val[1]

    charges = [re.sub(r' -', '', re.sub(r'ch.*?\d\s-\s', '', charge.text.lower()))
               for charge in d.find_element_by_xpath('//*[@id="MainContent_chargeDiv"]')
               .find_elements_by_tag_name('h1')]

    d.close()
    d.switch_to.window(d.window_handles[0])

    print('name: ', name, ' due: ', due, end='')

    with jsonlines.open('felo_data.jsonl', 'a') as writer:

        temp_json = {

            'id': case,
            'name': name,
            'dob': dem_table['DOB'],
            'race': dem_table['Race'],
            'sex': dem_table['Sex'],
            'category': category,
            'status': status,
            'ucn': ucn,
            'arrest_rpt_num': arrest_rpt,
            'due': due,
            'arrest_date': arrest_date,
            'close_date': close_date,
            'charges': charges

        }

        writer.write(temp_json)

        return True
