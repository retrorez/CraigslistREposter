#! python3

# Craigslist Posting Tool - Program will monitor email inbox and wait for
# emails from Realtor. When found, it will scrape the email for info
# and then use Selenium-controlled Firefox to navigate CList and post 
# the property

import readEmail
import requests, pyautogui, time
import smtplib
import imaplib
import email
import base64
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from apiclient import errors


##browser = webdriver.Firefox()
##pictures_folder = 'C:\\code\\python\\CraigslistPoster\\Pictures'

#Should be database! Very temporary!
completed_postings = []
################ Email Reader #################

# messages are in raw format from Google 
messages = readEmail.main()


# Create function that checks message ID against database of completed ID's
# If message ID is not in list of compelted ID's, create new listing

###################################################

def htmlToText(html):
    soup = BeautifulSoup(html, 'html5lib')
    
    #removing scripts, styles and other useless tags
    [element.extract() for element in soup(['style','script','meta','[document]','head','title'])]

    #getting text from html
    text = soup.getText()

    #removing leading/trailing spaces
    lines = [line.strip() for line in text.splitlines()]

    return text

def createPosting(emailMsg):

    
    content = emailMsg["raw"]
    html = base64.urlsafe_b64decode(content)
    emailBody = htmlToText(html)
    print(emailBody)
    
    # Login Credentials for Clist
    login = 'retrorezstudios@gmail.com'
    password = 'Thisismynewstupidfuckingpassword!'

    # Property Details
    state = 'FL'
    city = 'Hollywood'
    sub_city = ''
    zipcode = 33024
    posting_title = 'Beautiful 3 Bedroom Townhome'
    description = 'Beautiful Home for Rent'

    # Posting Details
    price = 1200
    sqft = 3200

    # Types: h = House, a = Apt, c = Condo, t = Townhouse
    house_type = 'a'

    # Laundry: 1 = WD in Unit, 2 = WD Hookups, 3 = Laundry in Bldg
    # 4 = Laundry on Site 5 = No Laundry on Site 
    laundry = 2

    # Parking: 1 = Carport, 2 = Att. Garage, 3 = Det. Garage
    # 4 = Offstreet Parking, 5 = Street Parking, 6 = Valet
    # 7 = No Parking
    parking = ''

    # Bedrooms: 0-8 Available
    bedrooms = 3

    # Bathrooms: Shared, Split, 1-8 w/ .5 option, 9+
    bathrooms = 2.5

    # Checkboxes
    dogsOK = True
    catsOK = True
    furnished = False
    smoking = False
    wheelchair = True

    # Availability will auto format Date, this is ending format
    avail = 'Sun, 24 Mar 2019'

    # Contact Info Section
    contact_email = 'retrorezstudios@gmail.com'
    contact_by_phone = True
    contact_by_text = True
    contact_phone = 7545551234
    contact_phone_ext = ''
    contact_name = "Retro Rex"

    #Location Info Section
    loc_street = ''
    loc_cross_street = ''
    loc_city = city


#########################################

################# Email Parser ################

for message in messages:
    if message['id'] not in completed_postings:
        createPosting(message)
                
###############################################
"""
#Start Creating Listing

#find the appropriate craigslist category with help from google
separator = '+'
location = [city, state, 'craigslist']
search_term = separator.join([city, state, 'craigslist'])

browser.get('https://www.google.com/search?q=' + search_term)
found_city_elem = browser.find_element_by_css_selector('.r a')
found_city_elem.click() 
browser.implicitly_wait(100)

# Begin the posting process
new_posting = browser.find_element_by_link_text('create a posting')
new_posting.click()

# pause for page load
browser.implicitly_wait(100)

# Login to Craigslist
post_type = browser.find_element_by_link_text('log in')
post_type.click()
post_type = browser.find_element_by_id('inputEmailHandle')
post_type.send_keys(login)
post_type = browser.find_element_by_id('inputPassword')
post_type.send_keys(password)
post_type = browser.find_element_by_id('login')
post_type.click()


# Check for subcats
try:
    subcats = browser.find_element_by_name('n')
    subcats.click()
except:
    print('no subcats!')

# Choose type of posting
try:
    post_type = browser.find_element_by_xpath('//input[@value="ho"]')
    post_type.click()
except:
    print('Couldnt find the radio button.')

# Choose housing/apts for rent
try:
    post_type = browser.find_element_by_xpath('//input[@value="1"]')
    post_type.click()
except:
    print('Couldnt find the radio button.')

# Begin Creating Posting

try:
    post_type = browser.find_element_by_id('PostingTitle')
    post_type.send_keys(posting_title)
except:
    print('Couldnt find the element.')

try:
    post_type = browser.find_element_by_id('GeographicArea')
    post_type.send_keys(city)
except:
    print('Couldnt find the element.')

try:
    post_type = browser.find_element_by_id('postal_code')
    post_type.send_keys(zipcode)
except:
    print('Couldnt find the element.')

try:
    post_type = browser.find_element_by_id('PostingBody')
    post_type.send_keys(description)
except:
    print('Couldnt find the element.')

try:
    post_type = browser.find_element_by_name('price')
    post_type.send_keys(price)
except:
    print('Couldnt find the element.')

try:
    post_type = browser.find_element_by_name('Sqft')
    post_type.send_keys(sqft)
except:
    print('Couldnt find the element.')

try:
    if house_type != '':
        post_type = browser.find_element_by_id('ui-id-1-button')
        post_type.click()
        post_type.send_keys(house_type)
        post_type.send_keys(Keys.RETURN)
    if laundry != 0:
        post_type = browser.find_element_by_id('ui-id-2-button')
        for i in range (laundry - 1):
            post_type.send_keys(Keys.DOWN)
        post_type.send_keys(Keys.RETURN)
    if parking != '':
        post_type = browser.find_element_by_id('ui-id-3-button')
        for i in range (parking - 1):
            post_type.send_keys(Keys.DOWN)
        post_type.send_keys(Keys.RETURN)
    
    # Input Bedrooms
    post_type = browser.find_element_by_id('Bedrooms-button')
    post_type.send_keys(bedrooms)

    # Input Bathrooms
    post_type = browser.find_element_by_id('ui-id-4-button')
    try:
        bathrooms = Math.ceil(bathrooms)
    except:
        bathrooms = str(bathrooms)
        bathrooms = bathrooms[0]
    
    post_type.send_keys(bathrooms)
    post_type.send_keys(Keys.TAB)

    # Checkboxes Section
    try: 
        if(catsOK):
           post_type = browser.find_element_by_name('pets_cat')
           post_type.click()
        if(dogsOK):
            post_type = browser.find_element_by_name('pets_dog')
            post_type.click()
        if(furnished):
            post_type = browser.find_element_by_name('is_furnished')
            post_type.click()
        if(smoking):
            post_type = browser.find_element_by_name('no_smoking')
            post_type.click()
        if(wheelchair):
            post_type = browser.find_element_by_name('wheelchaccess')
            post_type.click()
    except:
        print('Failed at Desc. Checkboxes')
    
    # Availability Section
    try:
        post_type = browser.find_element_by_xpath('//input[@placeholder="select date"]')
        post_type.send_keys(avail)
        post_type.send_keys(Keys.TAB)
    except:
        print('Failed at Availability Section')

    try:
        if(contact_by_phone):
            post_type = browser.find_element_by_name('contact_phone_ok')
            post_type.click()
        if(contact_by_text):
            post_type = browser.find_element_by_name('contact_text_ok')
            post_type.click()
    except:
        print('Failed at contact area')

    post_type = browser.find_element_by_name('contact_phone')
    post_type.send_keys(contact_phone)
    if contact_phone_ext != '':
        post_type = browser.find_element_by_name('contact_phone_extension')
        post_type.send_keys(contact_phone_extension)
    post_type = browser.find_element_by_name('contact_name')
    post_type.send_keys(contact_name)
    post_type = browser.find_element_by_name('city')
    post_type.send_keys(loc_city)

    # Go to Next Step
    post_type = browser.find_element_by_name('go')
    post_type.click()

    # Confirm Map Location
    post_type = browser.find_element_by_xpath('//button[@class="continue bigbutton"]')
    post_type.click()

    # Pictures Section - by this point pictures should be in hard drive in specified root folder 'pictures_folder'
    post_type = browser.find_element_by_id('plupload')
    post_type.click()
    
except:
    print('Couldnt find the element.')


# This part is Windows-based to select photos, steps away from Selenium for a moment

for i in range(5):
    pyautogui.press('tab', interval=1)
pyautogui.press('space')
pyautogui.typewrite(pictures_folder)
pyautogui.press('enter')
for i in range(5):
    pyautogui.press('tab', interval=1)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('enter')

# Back to Selenium, confirm pictures after waiting for load
time.sleep(18)
pyautogui.press('pagedown')

#This worked but not everytime. Defintely optimize
try:
    post_type = browser.find_element_by_xpath('//button[@value="Done with Images"]')
    post_type.click()
except:
    print('failed at Done With Images button')

# Final Publishing Page
#Check for final puclish button, otherwise email must be checked for Final Step
try:
    post_type = browser.find_element_by_xpath('//button[@value="Continue"]')
    post_type.click()
except:
    print('Failed at final step')
    #Open Email
    #Click Link
    #Find Publish Button


#Check for Publish Requirement
#try:
    #post_type = browser.find_element_by_


#Upon Completion of Listing, add message ID to list of completed listings
completed_listings.append(message['id'])
completed_listings.sort()

"""
