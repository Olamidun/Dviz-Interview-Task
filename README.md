*Edmund.com Vehicle Details Scraper*
This is a script that automates scraping of details of vehicle on edmund.com. It scrapes the name, price, vin number, top features and spec, and the vehicle summary

*Technologies Used*
* Python
* Selenium
* Web driver manager

*How To Use*
navigate to the src folder of the project and run `python scrape_script.py`, enter the zipcode to narrow down the list of cars that will be returned for us. Ensure you have a fast and stable internet connection as absence of this will affect the running of the script.

Because of time constraint, the script can only scrape the vehicle details of all the vehicles returned in the first page, i.e pagination wasn't handled. Also option for user to input the radius of search wasn't implemented.

