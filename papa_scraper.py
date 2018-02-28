#import needed modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

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
def get_owner_name(list):

    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    br = webdriver.Firefox(capabilities=firefox_capabilities)
    owner_names = {}
    delay = 20

    for address in list:
        #access page we want to start on
        br.get('http://www.pbcgov.com/papa/')
        no_owner_name = False

        #check if on correct page
        assert 'Property Appraiser, Palm Beach County, Florida, USA' in br.page_source
        
        #switch to the iframe with the elements we are interested in
        iframeSrch = WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'frameSrch')))
        br.switch_to.frame(iframeSrch)

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
            br.find_element_by_xpath("//td[contains(text(), '%s')]" % address[0:4]).click()
            
        #no search results page
        elif search_results is None and 'PropertyDetail' not in br.current_url:
            no_owner_name = True
            WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'MainContent_btnBackToSrchTop'))).click()
            continue

        #property info page
        myElem = WebDriverWait(br, delay).until(EC.presence_of_element_located((By.ID, 'MainContent_gvOwners')))
        
        owner_name_arr = myElem.text.split('\n')

        if no_owner_name is False:
            owner_name = owner_name_arr[1]
        else:
            owner_name = 'N/a'

        #format owner name
        formatted_name = format_name(name=owner_name).split(' ')

        if owner_name is not None:
            owner_names[address] = [formatted_name[0], formatted_name[1]]
            print owner_names
        else:
            print None
            
    return owner_names

#write to csv document            
def write_to_csv(info, file_name):

    #create file
    file_object = open(file_name, 'w+')

    column_title = 'Property Address, First Name, Last Name\n'
    file_object.write(column_title)

    #write info from input array
    for key in info.keys():
        row = key + ', ' +info[key][0] + ', ' + info[key][1] + '\n'
        file_object.write(row)

    #close the file
    file_object.close()
    
address_list = [
'13 Alnwick Road',
'3456 Collonade Drive',
'ppp',
'29 Milestone Way',
'5940 Westfall Road',
'107 S Hampton Drive',
'35 E 25th Street',
'130 Peabody Drive',
'510 Jaeger Drive',
'8729 Wellington View Drive',
'7967 Mandarin Boulevard',
'21910 Pine Trace',
'11090 Clover Leaf Circle',
'11008 La Salinas Circle',
'9406 Silent Oak Circle',
'3416 NW 51st Place',
'5627 120th Avenue N',
'619 Castle Drive',
'2845 W Foxhall Drive',
'8170 Santalo Cove Court',
'5600 Old Orange Road',
'2146 Bellcrest Circle',
'12503 Shoreline Drive',
'3760 Learwood Drive',
'6951 NE 7th Avenue',
'521 NE 32nd',
'5322 Garden Hills Circle',
'3620 Royal Tern Circle',
'7603 San Carlos Street',
'14844 Gruber Lane',
'10289 Isle Wynd Court',
'12403 Cascades Pointe Drive',
'133 Cypress Drive',
'1019 N K Street',
'17561 69th Street N',
'6579 Rainwood Cove Lane',
'123 Isola Circle',
'112 Heather Lane',
'222 Columbia Drive',
'8973 Lakes Boulevard',
'622 Castle Dr',
'2490 NW 63rd Street',
'526 NW 13th Drive',
'132 Pembroke Drive',
'7548 Eagle Point Drive',
'101 Emerald Key Lane',
'1180 Oakwater Drive',
'2675 Reids Cay',
'509 NW 54th Street',
'19569 Sedgefield Terrace',
'11571 Big Sky Court',
'15733 88th Place  N',
'481 Pine Tree Court',
'1351 SW 27th Avenue',
'16243 E Yorkshire Drive',
'150 W 31st Court',
'305 SW 3rd Street',
'602 N Cypress Drive',
'5255 Brookview Drive',
'145 SE 8th Avenue',
'5449 White Sands Cove',
'734 SE 4th Avenue',
'12181 148th Road N',
'6491 Park Lane W',
'1756 Seminole Pratt Whitney Road',
'1341 SW 26th Avenue',
'3028 Casa Rio Court',
'924 Quartz Ter',
'355 NE 6th Street',
'4065 Wellington Shore Drive',
'10130 Fanfare Drive',
'711 N E Street',
'3162 Hamblin Way',
'1735 Newhaven Point Lane',
'14418 Paddock Drive',
'1206 General Pointe Trace',
'6484 Via Benita',
'13693 Carlton Street',
'13610 Cambria Bay Lane',
'5727 Sandbirch Way',
'7087 Corning Circle',
'109 SE 29th Avenue',
'3888 Tracewood Lane',
'315 11th Street',
'4780 Todd Street',
'3712 Miramontes Circle',
'107 Rivera Avenue',
'11552 Paradise Cove Lane',
'333 Eagle Drive',
'19931 Oslo Court',
'1417 W 33rd',
'8030 Inagua Lane',
'1906 SW 13th Terrace',
'310 Valencia Road',
'12525 Persimmon Boulevard',
'757 Orchid Drive',
'2078 Chagall Circle',
'10745 Locust Street',
'17394 61st Place',
'1920 Cambodiana Road',
'4745 Nolina Lane',
'1064 W 26th Court',
'6667 S Pine Court',
'10681 Richfield Way',
'7069 Haviland Circle',
'12280 Riverfalls Court',
'4714 Arlette Court',
'116 NE 15th Avenue',
'12406 86th Road N',
'2692 Acklins Road',
'904 Flamango Lake Court W',
'2403 Dorson Way',
'4596 Holly Lake Drive',
'340 Vizcaya Drive',
'20894 Sugarloaf Lane',
'6536 Compass Rose Court',
'24 Burning Tree Lane',
'8642 Tierra Lago Cove',
'11288 Orange Grove Boulevard',
'20100 Ocean Key Drive',
'802 N C Street',
'6567 Venetian Drive',
'204 Seagull Point',
'1415 N Palmway',
'11629 Kensington Court',
'10184 Spyglass Way',
'3761 Dellwood Road',
'15885 87th Road N',
'10108 Windtree Lane',
'3095 Swain Boulevard',
'418 SW 15th Avenue',
'21431 Sawmill Court',
'1650 NE 3rd Avenue',
'118 Bianca Drive',
'11389 Sandstone Hill Ter',
'232 Longshore Drive',
'1161 Dakota Drive',
'4637 Poseidon Place',
'421 SW 7th Avenue',
'22479 Sea Bass Drive',
'1035 W 25th Street',
'816 Lincoln Court',
'139 E Central Boulevard',
'1084 Aspri Way',
'1770 22nd Avenue N',
'5275 Park Place Circle',
'24 Thurston Drive',
'16141 E Aquaduct Drive',
'15799 88th Trail N',
'115 Isle Verde Way',
'3502 Lake Osborne Drive',
'2938 Donald Road',
'843 Upland Road',
'437 Woodview Circle',
'18730 Rio Vista Drive',
'2110 SW 23rd Court',
'9911 Harbour Lake Circle',
'306 Vallette Way',
'9601 Majestic Way',
'3094 Hartridge Terrace',
'4651 Holly Drive',
'934 SW 34th Court',
'21836 Reflection Lane',
'1357 Sailboat Circle',
'416 Monroe Drive',
'9433 Via Elegante',
'9373 Via Elegante',
'21130 White Oak Avenue',
'6570 Timber Lane',
'3425 Vanderbilt Drive',
'4271 NW 64th Lane',
'509 Lighthouse Drive',
'108 Banyan Lane',
'2565 Canterbury',
'11326 Clover Leaf Circle',
'9077 Alexandra Circle',
'10706 165th Road N',
'7770 Colony Lake Drive',
'1650 45th Street',
'2131 NE 4th Avenue',
'7203 Arcadia Bay Court',
'6334 NW 24th Street',
'1502 NW 4th Avenue',
'19473 Preserve Drive',
'7872 L Aquila Way',
'7315 Greenport Cove',
'5813 Dewberry Way',
'5136 Van Buren Road',
'9075 Dupont',
'9030 Equus Circle',
'415 Park Avenue',
'5496 NW 20th Avenue',
'1555 SW 4th Circle',
'4402 N San Andros',
'168 Jones Creek Drive',
'6917 Barnwell Drive',
'17809 Southwick Way',
'22732 SW 10th Street',
'14701 Smokey Citrine Street'
]

owners = get_owner_name(list=address_list)

#write to a csv document
write_to_csv(owners, '/home/andre/Documents/owner_names2.csv')
