from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import json

chromedriver = '/usr/lib/chromium-browser/chromedriver'
driver = webdriver.Chrome(chromedriver)

url = 'https://www.facebook.com/pg/quattromiami/reviews/'

driver.get(url)
#sort by most recent
driver.find_elements_by_class_name('_3m1v')[1].send_keys(keys.Keys.SPACE)
javascript = """
var see_more_href= 'https://www.facebook.com/ajax/pages/review/spotlight_reviews_tab_pager/?cursor=1191066409%3A147525207605&fetch_on_scroll=0&max_fetch_count=100000&page_id=147525207605&sort_order=most_recent';
var see_more = document.getElementsByClassName('pam uiBoxWhite noborder uiMorePagerPrimary')[0];
see_more.href=see_more_href;
see_more.click();
"""
driver.execute_script(javascript)

#wait for new reviews to load
timeout = 45 # seconds
try:
    element_present = EC.presence_of_element_located((By.ID, 'u_6_f9'))
    WebDriverWait(driver, timeout).until(element_present)
    print "Page is ready for scraping."
except TimeoutException:
    print "Loading took too much time."

element_present = EC.presence_of_element_located((By.ID, 'u_5_1o'))
WebDriverWait(driver, timeout).until(element_present)
reviews = driver.find_element_by_id('most_recent_list').find_elements_by_class_name('_4-u2')

for review in reviews:
    review_info = {}
    try:
        social = review.find_elements_by_class_name('_2u_j')
        if social:
            review_info['likes'] = social[0].text[0]
        if 1 < len(social):
            review_info['comments'] = social[1].text[0]
    except NoSuchElementException:
        pass

    profile_links = review.find_elements_by_class_name('profileLink')
    review_info['reviewer_name'] = profile_links[0].text
    review_info['reviewer_profile_link'] = profile_links[0].get_attribute('href')
    review_info['page_link'] = profile_links[1].get_attribute('href')
    review_info['reviewer_profile_image'] = review.find_element_by_class_name('_s0').get_attribute('src')
    review_info['reviewer_content'] = review.find_element_by_class_name('userContent').text
    review_info['timestamp'] = review.find_element_by_class_name('timestampContent').text
    review_info['rating'] = review.find_element_by_class_name('_51mq').find_element_by_tag_name('u').text[0]
    review_info = json.dumps(review_info)
    print(review_info)
