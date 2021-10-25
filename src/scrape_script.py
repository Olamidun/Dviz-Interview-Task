import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager


# This code block is used to write the header for the csv file
with open('dviz_data.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ['Name', 'Price', 'VIN', 'Vehicle Summary', 'Top Features & Specs']
    writer.writerow(header)


class VehicleInfoClass:

    # method which makes use of selenium to scrape vehicle info
    def scrape_vehicle_details(self):
        zipcode = int(input("Enter your zipcode: "))
        count = 1 # This is what will be used to differentiate between the vehicles in the vehicle listing page.

        url = f'https://www.edmunds.com/cars-for-sale-by-owner/'

        options = Options() # Initialize the options class which is one of the arguments that will be used in webdriver.Chrome class
        options.headless = False # This is set to false so we can see how the scraping is done via the website UI
        options.add_experimental_option("detach", True)

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options) # class that install chromedriver. ChromeDriverManager().install() ensures the latest version of the chrome driver is installed
        browser.maximize_window() # This maximizes the browser window to full screen
        browser.get(url)
        browser.set_page_load_timeout(45) # If the page does not load within the value passed into the function, it returns a timeout error.

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
        action.move_to_element(zipcode_form).click(zipcode_form).click(zipcode_form).send_keys(Keys.DELETE).send_keys(str(zipcode)).perform()

        '''
        
        While Loop to go back and forth the car listing page and the car details page
        
        '''

        # /html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/div[2]/div[2]/span
        while True:
            listing = browser.find_element_by_css_selector('span.text-nowrap.medium.text-gray')
            convert_listing_max_to_int = int(listing.text.split(' ')[3]) # This is to get the number of cars that is being returned on the first page and the convert it to int so I can use that to get out of the while loop once the that number of car details has been scrapped.
            try:
                # We are the using the variable in comparison with the count varible. So if count is less than or equal, it should continue scrapping the vehicle details
                if count <= convert_listing_max_to_int:
                    '''
                    We are getting each car in the car listing page and then clicking on it. We are doing this by making use of the xpath of the anchor tag, this is so we can click on it and then it takes us to the car details page. This is where I am making use of the count variable I declared above. I am declaring the WevDriverWait to wait for the element that houses the car name to be located by the webdriver before it continue scraping, this is because it some times take a while to load.

                    '''
                    WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/ul/li[{str(count)}]/div/div[2]/div/h2/a")))
                    car = browser.find_element_by_xpath(f"/html/body/div[1]/div/main/div[3]/div[1]/div[1]/div/ul/li[{str(count)}]/div/div[2]/div/h2/a").click()

                    # car_name_xpath = '//div[@name='overview'/h1'

                    # This is used to get the car name in the vehicle details page
                    car_name = browser.find_element_by_css_selector('h1.not-opaque.text-black.d-inline-block.mb-0.size-24')

                    # This is used to get the car name details in the vehicle details page also
                    car_name_details = browser.find_element_by_css_selector('span.not-opaque.text-black')

                    car_full_name = f'{car_name.text} {car_name_details.text}'

                    car_price = browser.find_element_by_css_selector("div.heading-2.mb-0")

                    # Gets the VIN number of the vehicle from the vehicle details page
                    vin_number = browser.find_element_by_css_selector("span.mr-1")

                    '''the vehicle summary returns a list, so I am looping through the list to get each items in the lsit to extract their test. I am appending them to a list which will be path of the data saved in the csv file'''
                    vehicle_summary = browser.find_elements_by_css_selector("div.m-0.mb-1.row")
                    vehicle_summary_list = []
                    for info in vehicle_summary:
                        vehicle_summary_list.append(info.find_element_by_css_selector("div.col").text)

                    
                    '''the top features and specs element also returns a list, so I am looping through the list to get each items in the list to extract their test. I am appending them to a list which will be path of the data saved in the csv file'''
                    top_features_and_specs = browser.find_elements_by_css_selector("li.mb-0_5")

                    top_features_and_specs_list = []
                    for summary in top_features_and_specs:
                        top_features_and_specs_list.append(summary.text)

                    data = [car_full_name, car_price.text, vin_number.text, vehicle_summary_list, top_features_and_specs_list]
                    with open('dviz_data.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(data)
                    print(F'--------SCRAPPING FOR VEHICLE {count}------------')

                    url = f'https://www.edmunds.com/cars-for-sale-by-owner/'
                    browser.get(url)
                    browser.set_page_load_timeout(45)
                    count += 1
                     # This increases the count by 1 so selenium knows to click on the next car
                else:
                    print("Scrapping is done!!")
                    break
            except Exception as e:
                print(e)

        read_file = pd.read_csv('dviz_data.csv') # This is a panda function that reads a csv file, which we will convert into an excel workbook
        read_file.to_excel('dviz_data.xlsx', index=None, header=True) # This function converts a csv file into an excel workbook
        browser.close()

# This converts this csv file into an excel workbook
scrapped_vehicle_info = VehicleInfoClass() # Instantiating the class so we can access the method defined in it

scrapped_vehicle_info.scrape_vehicle_details()




