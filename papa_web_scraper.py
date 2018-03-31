#import needed modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import os

#format names
def format_name(name):
    #remove ampersands
    new_name = name.replace('&', '')

    #put first name first and last name after
    new_name_arr = new_name.split(' ')

    full_name = new_name_arr[1] + ' ' + new_name_arr[0]

    #proper case
    full_name = full_name.title()

    return full_name

#gets owner name from the PAPA apprasier website
def get_owner_name(addresses):

    #firefox_capabilities = DesiredCapabilities.FIREFOX
    #firefox_capabilities['marionette'] = True

    #br = webdriver.Firefox(capabilities=firefox_capabilities)
    CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
    br = webdriver.Chrome(CHROMEDRIVER_PATH)
    owner_info = {}
    delay = 20

    for address in addresses:
        #access page we want to start on
        br.get('http://www.pbcgov.com/papa/')
        no_owner_name = False

        #check if on correct page
        assert 'Property Appraiser, Palm Beach County, Florida, USA' in br.page_source

        #switch to the iframe with the elements we are interested in
        iframeSrch = WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'frameSrch')))
        br.switch_to.frame(iframeSrch)

        #interact with search elements
        #interact with search elements
        br.find_element_by_id('imgAddress').click()
        br.find_element_by_id('txtAddress').send_keys(address)
        br.find_element_by_id('btnAddressSrch').click()

        #switch to document root when finished interacting with iframe elements
        br.switch_to.default_content()

        #pages we end up on after searching for the address

        try:
            search_results = br.find_element_by_id('gvSrchResults')
        except NoSuchElementException:
            search_results = None

        #if we end up on a page with multiple addresses
        if search_results is not None:
            try:
                br.find_element_by_xpath("//td[contains(text(), '%s')]" % address[0:5]).click()
            except NoSuchElementException:
                print('Address not found in address list')
                continue
            
        #no search results page
        elif search_results is None and 'PropertyDetail' not in br.current_url:
            no_owner_name = True
            WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'MainContent_btnBackToSrchTop'))).click()
            continue

        #property info page
        #owner name
        owner_name_elem = WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'MainContent_gvOwners')))
        owner_name_arr = owner_name_elem.text.split('\n')
        owner_name = owner_name_arr[1]

        #mail address
        mail_address_1 = br.find_element_by_id('MainContent_lblAddrLine1').text
        mail_address_3 = br.find_element_by_id('MainContent_lblAddrLine3').text
        mail_address = mail_address_1 + ' ' + mail_address_3

        #format owner name
        formatted_name = format_name(name=owner_name).split(' ')

        owner_info['Owner'] = [formatted_name[0], formatted_name[1]]
        owner_info['Property Address'] = address
        owner_info['Mail Address'] = mail_address.title()

        #write to csv
        csv_path = '/home/andre/Documents/owner_names2.csv'
        write_to_csv(owner_info, csv_path)
        print(owner_info)

def write_to_csv(info, file_name):

    #create file
    file_object = open(file_name, 'a+')

    # write column titles if file is empty
    if os.stat(file_name).st_size == 1:
        column_titles = 'Property Address,First Name,Last Name,Mail Address\n'
        file_object.write(column_titles)

    #write info from input dictionary
    row = info['Property Address'] + ',' +info['Owner'][0] + ',' + info['Owner'][1] + ',' + info['Mail Address'] + '\n'
    file_object.write(row)     

    #close the file
    file_object.close()

#get info from downloaded csv
csv_path = '/home/andre/Downloads/textexport.csv'
addresses = []
with open(csv_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        address = [
            line['Street #'], line['Street Dir'],
            line['Street Name'], line['Unit #'],
            line['Street Post Dir'], line['Street Suffix'],
            'FL', line['City'], line['Zip Code'],
        ]
        #remove trailing white space and empty strings
        address = [x.strip() for x in address]
        address = list(filter(None, address))
        address = ' '.join(map(str, address))
        addresses.append(address)

get_owner_name(addresses=addresses)
