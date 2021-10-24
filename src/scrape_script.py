from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager 

# 'https://www.edmunds.com/inventory/srp.html?inventorytype=used%2Ccpo&wz=73&radius=75'


def scrape_car_details():
    radius = int(input("Enter the radius: "))
    zipcode = int(input("Enter your zipcode: "))
    count = 1
    page = 1

    url = f'https://www.edmunds.com/cars-for-sale-by-owner/'
    # url = f'https://www.edmunds.com/inventory/srp.html?radius={str(radius)}&wz={str(zipcode)}'

    options = Options() # Initialize the options class which is one of the arguments that will be used in webdriver.Chrome class
    options.headless = False # This is set to false so we can see how the scraping is done via the website UI
    options.add_experimental_option("detach", True)

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options) # class that install chromedriver. ChromeDriverManager().install() ensures the latest version of the chrome driver is installed
    browser.maximize_window() # This maximizes the browser window to full screen
    browser.get(url)
    browser.implicitly_wait(10)
    browser.set_page_load_timeout(15)

    '''
    This is to ensure that the zipcode input field has been loaded and can be clicked before we attempt to find the input field. We are getting the input field because we need to pass in our own zipcode.
    '''
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.NAME, 'zip')))
    zipcode_form = browser.find_element_by_name('zip') # this finds the zipcode input field

    '''
    
    ActionChains is used to perform some low-level interaction with the webpage. Such interactions include hover, mouse movements, key press, clicks. It can also be used to fill in a form.

    In our case we want to clear the default zipcode in the zipcode input field and then use the zipcode entered by the user.

    '''
    action = ActionChains(browser)
    action.move_to_element(zipcode_form).click(zipcode_form).click(zipcode_form).send_keys(Keys.DELETE).send_keys('85001').perform()

    '''
    
    While Loop to go back and forth the car listing page and the car details page
    
    '''
    while True:
        try:
            '''
            We are getting each car in the car listing page and then clicking on it. We are doing this by making use of the xpath of the anchor tag, this is so we can click on it and then it takes us to the car details page

            '''
            car = browser.find_element_by_xpath(f"/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/ul/li[{str(count)}]/div/div[2]/div/h2/a").click()

            # car_name_xpath = '//div[@name='overview'/h1'

            # This is used to get the car name in the vehicle details page
            car_name = browser.find_element_by_css_selector('h1.not-opaque.text-black.d-inline-block.mb-0.size-24')

            # This is used to get the car name details in the vehicle details page also
            car_name_details = browser.find_element_by_css_selector('span.not-opaque.text-black')

            car_price = browser.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[2]/div/div[1]/div[4]/section[1]/div[2]/form/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/div")

            # Gets the VIN number of the vehicle from the vehicle details page
            vin_number = browser.find_element_by_css_selector("span.mr-1")

            print(car_name.text)
            print(car_name_details.text)
            print(car_price.text)
            print(vin_number.text)

            vehicle_summary = browser.find_elements_by_css_selector("div.m-0.mb-1.row")
            for info in vehicle_summary:
                print(info.find_element_by_css_selector("div.col").text)

            top_features_and_specs = browser.find_elements_by_css_selector("li.mb-0_5")

            for summary in top_features_and_specs:
                print(summary.text)

            print(F'--------PRINTING FOR {count} PAGE------------')

            url = f'https://www.edmunds.com/cars-for-sale-by-owner/'
            browser.get(url)
            browser.set_page_load_timeout(15)
            count += 1

        except Exception as e:
            print(e)

scrape_car_details()
