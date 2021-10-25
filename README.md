# [edmund.com](https://www.edmunds.com/cars-for-sale-by-owner/) Vehicle Details Scraper
This is a script that automates scraping of details of vehicle on edmund.com. It scrapes the name, price, vin number, top features and spec, and the vehicle summary

# Technologies Used
* Python
* Selenium
* Web driver manager
* Pandas

# How To Use
run `pip install -r requirements.txt` to install all the dependency needed to run this project.
Navigate to the src folder of the project and run `python scrape_script.py`, enter the zipcode to narrow down the list of cars that will be returned.
The scraped data will be stored into a csv file which will then be converted into an excel workbook. The excel workbook will also appear in the src folder when the script executes completely.

Ensure you have a fast and stable internet connection as absence of this will affect the running of the script. 

Because of time constraint, the script can only scrape the vehicle details of all the vehicles returned in the first page, i.e pagination wasn't handled. Also option for user to input the radius of search wasn't implemented.

