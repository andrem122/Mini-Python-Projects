"""Gets 3 images from the url"""
#import needed modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from mimetypes import guess_extension
import requests, os

#set up web browser
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
br = webdriver.Firefox(capabilities=firefox_capabilities)

def get_or_create_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)
    else:
        os.chdir(name)

"""Creating dirs"""     
#cd into twitter_content
get_or_create_dir('twitter_content')
#cd into twitter_images
get_or_create_dir('twitter_images')


"""Scraping images"""
#go to web page
br.get('https://www.pexels.com/search/real%20estate%20house/')

#get first 3 images
imgs = br.find_elements_by_xpath('//img[@class="photo-item__img"]')[:3]

#download images
i = 0
for img in imgs:
    img_src = img.get_attribute('src')

    try:
        source = requests.get(img_src)
        if source.status_code == 200:
            image_name = 'image-' + str(i) + '.' + '.jpg'
            with open(image_name, 'wb') as f:
                f.write(requests.get(img_src).content)
                i += 1
        else:
            print('Error: URL could not be retrieved')
    except:
        print('Error: Image could not download')
        pass
