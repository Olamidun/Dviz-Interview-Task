import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class crawledInfo():
    def __init__(self, title, price, summary, options):
        self.title = title
        self.price = price
        self.summary = summary
        self.options = options


class bot:

    def scraper():

        count = 1

        radius = str(input("what is your preffered radius?"))
        zipCode = str(input("what is your preffered ZipCode?"))

        url = f"https://www.tred.com/buy?body_style=&amp;distance=&amp;exterior_color_id=&amp;make=&amp;miles_max=100000&amp;miles_min=0&amp;model=&amp;page_size=24&amp;price_max=100000&amp;price_min=0&amp;query=&amp;requestingPage=buy&amp;sort=desc&amp;sort_field=updated&amp;status=active&amp;year_end=2022&amp;year_start=1998&amp;zip="

        # Create a new instance of the Chrome driver
        options = Options()
        options.headless = False
        options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        browser.maximize_window()
        browser.get(url)
        browser.set_page_load_timeout(10)

        # print url to confirm
        print(url)

        data = []
        while True:
            try:
                cars = browser.find_element_by_xpath(f'//*[@id="cars"]/div/div/div[1]/div/div[{str(count)}]/div/div/div/a').click()

                    # //*[@id="cars"]/div/div/div[1]/div/div[4]/div/div/div/a
                    # //*[@id="cars"]/div/div/div[1]/div/div[1]/div/div/div/a

                # get title of car
                # xPathTitle = '//*[@id="header-box"]/div/div/div[1]/div/h2[1]'
                title = browser.find_element(By.CSS_SELECTOR, 'h1.bigger.small-top-margin.visible-xs')
                titleText = title.get_attribute("innerHTML")
                print(titleText)

                # get price of car
                xPathPrice = '//*[@id="header-box"]/div/div/div[2]/div/div/h2'
                price = browser.find_element_by_xpath(xPathPrice)
                priceText = price.get_attribute("innerHTML")

                # get summary of car
                xPathSummary = '# summary-table'
                summary = browser.find_element_by_xpath(xPathSummary)
                summaryText = summary.get_attribute("innerHTML")

                # get options of car
                xPathOptions = '# summary-table'
                options = browser.find_element_by_xpath(xPathOptions)
                optionsText = options.get_attribute("innerHTML")

                print(price.text, title.text, summary.text, options.text)

                browser.get(url)
                browser.set_page_load_timeout(10)

                info = crawledInfo(titleText, priceText,
                                   summaryText, optionsText)
                data.append(info)

                print(data)

                count += 1

                print(f'--------PRINTING FOR {count} ------------')

            except Exception as e:
                print(e)

                break

        browser.close()
        return data


bot = bot.scraper()

with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for article in bot:
        writer.writerow([article.title, article.price,
                        article.summary, article.options])