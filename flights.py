import time
from datetime import datetime, timedelta, date
import collections
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sendemail
import smtplib, ssl

class wait_for_date_prices(object):
    def __init__(self, locator, text_length):
        self.locator = locator
        self.text_length = text_length

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        returned_elements = []
        for element in elements:
            if len(element.get_attribute('innerText')) > 0:
                returned_elements.append(element)
        return returned_elements if returned_elements else False

month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# def send_email():
#     port = 465
#     password = 'Temp1!1337'
#     context = ssl.create_default_context()

#     with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#         server.login("

def lookup_flights(driver, trip_duration: int, start_date):
    """
    This function uses selenium to look up flights on google.com/travel/flights 
    using the start date and the duration to find prices. Right now, the link to google
    is set up for Delta flights only. #sponsored
    """

    today_split = str(start_date).split('-')
    today = month_options[int(today_split[1])-1] + ' ' + today_split[2]

    # month, day = today.split()

    end_date = datetime.now() + timedelta(days=trip_duration)
    end_date_split = str(end_date).split('-')
    end_date_split = [end_date_split[1], end_date_split[2][:2]]
    end_date_str = month_options[int(end_date_split[0])-1] + ' ' + end_date_split[1]
    depart_date_and_return_date = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.TP4Lpb.eoY5cb.j0Ppje'))
    )

    time.sleep(1)
    depart_date_and_return_date[0].click()
    time.sleep(1)
    depart_date_and_return_date[2].send_keys(today)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.z18xM.rtW97.Q74FEc.dAwNDc').click()
    time.sleep(1)
    depart_date_and_return_date[1].click()
    time.sleep(1)
    depart_date_and_return_date[3].send_keys(end_date_str)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.z18xM.rtW97.Q74FEc.dAwNDc').click()
    time.sleep(1)
    depart_date_and_return_date[0].click()

def Choose_Origin_and_Destination(driver, origin: str, destination: str) -> None:
    """
    Enter the origin airport and destination airport. Chromedriver enters these into the web interface
    and hits the 'search' button
    """

    # gets the 'Where from?' and 'Where to? ' fields
    # it returns 4 fields, including 'Where else' for both of the to and from fields.
    to_from = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.II2One.j0Ppje.zmMKJ.LbIaRd'))
    )

    # iterate through to find the origin and destination fields
    for field in to_from:
        print(field.get_attribute('aria-label'))
        if field.get_attribute('aria-label') == 'Where from?':
            origin_field = field
            origin_field.clear()
            origin_field.send_keys(origin)
            time.sleep(.8)
             # entering origin above causes a dropdown of suggestions to populate
             # have to select one from the dropdown for the destination field to be clickable.
            confirm_origin_field = driver.find_element(By.CSS_SELECTOR, '.n4HaVc')
            confirm_origin_field.click()
            time.sleep(.8)
        if field.get_attribute('aria-label') == 'Where to? ':
            destination_field = field
            destination_field.clear()
            destination_field.send_keys(destination)
            time.sleep(.8)
            # entering destination above causes a dropdown of suggestions to populate
            # have to select one from the dropdown for the search button to be clickable.
            confirm_destination_field = driver.find_element(By.CSS_SELECTOR, '.n4HaVc')
            confirm_destination_field.click()
            time.sleep(.8)

    time.sleep(.8)
    #select search to show calendar with dates
    search_button = driver.find_element(By.CSS_SELECTOR, '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.nCP5yc.AjY5Oe.LQeN7.TUT4y.zlyfOd')
    search_button.click()

def get_next_month_year(month_year: str) -> str:
    yyyy, mm, dddd = month_year.split('-')

    # get a calendar from '01' to '12'
    calendar = ['0' + str(i+1) if (len(str(i + 1)) == 1) else str(i + 1) for i in range(12)]

    next_month = (int(mm)) if int(mm) < 12 else 0
    mm = calendar[next_month]
    if mm == '01':
        yyyy = str(int(yyyy) + 1)
    print(mm)

    return yyyy + '-' + mm + '-'

def format_prices(dataframe):
    for column in dataframe.values.tolist():
        print(column)

def get_flight_prices():

# Setup the webdriver
    service = Service('./chromedriver')
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)

# Open the Google Flights page
# driver.get('https://www.google.com/travel/flights/')

    date_price_database = collections.defaultdict()

#go right to MCO to MSP
    driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhpGEgoyMDI0LTA5LTA1OgJBUzoCQUE6AkY5OgJCNjoCUVI6AkVLOgJXTjoCTks6AlNZOgJVQWoHCAESA01DT3IHCAESA01TUBpGEgoyMDI0LTA5LTA5OgJBUzoCQUE6AkY5OgJCNjoCUVI6AkVLOgJXTjoCTks6AlNZOgJVQWoHCAESA01TUHIHCAESA01DT0ABSAFwAYIBCwj___________8BmAEB&tfu=EgIIACIA')

# Wait for the necessary element to load (this may vary depending on what you need)
    try:

        today = date.today()
        lookup_flights(driver, 5, today)

        # get today's year/month as 'yy-mm'
        yyyy_mm = str(date.today())[:-2]
     
        # Selects all of the elements used in the calendar that have a date so we can use 
        # the dates in our price database
        dates = driver.find_elements(By.CSS_SELECTOR, '.WhDFk.Io4vne')

        for i in range (12):

            # This is a locator to find the prices under each date in the calendar
            locator = (By.CSS_SELECTOR, '[jsname="qCDwBb"]')


            print('waiting for elements')
            prices = WebDriverWait(driver, 10).until(wait_for_date_prices(locator, 3))
            print('elements loaded')

            i = 0
            while dates:
                
                next_date = dates[i]
                if int((yyyy_mm.split('-')[0])) < int(str(next_date.get_attribute('data-iso')).split('-')[0]):
                       break
                if int((yyyy_mm.split('-')[1])) < int(str(next_date.get_attribute('data-iso')).split('-')[1]):
                       break
                if yyyy_mm in str(next_date.get_attribute('data-iso')):
                    price = next_date.find_element(By.CSS_SELECTOR, '[jsname="qCDwBb"]')
                    if len((str(price.get_attribute('innerText')))) > 0:
                        date_price_database[next_date.get_attribute('data-iso')] = price.get_attribute('innerText')
                        dates.pop(0)
                        i -= 1
                    else:
                        dates.pop(0)
                        i -= 1

                i += 1
                if i == len(dates):
                    break

            #incrememt month and/or year appropriately
            yyyy_mm = get_next_month_year(yyyy_mm)

            # Go to next month
            next_month = driver.find_element(By.CSS_SELECTOR, '.d53ede.rQItBb.FfP4Bc.Gm3csc')
            if not next_month.is_displayed():
                print(dates)
                continue
            else:
                next_month.click()

    finally:
        new_dict = {}
        id = 0
        for entry in date_price_database:
            year, month, day = entry.split('-')
            price = date_price_database[entry]
            new_dict[id] = {'price': price, 'year': year, 'month': month, 'day': day}
            id += 1

        df = pd.DataFrame(new_dict).T
        df['price'] = df['price'].str.replace('$', '')
        df['price'] = df['price'].str.replace(',', '')
        df['price'] = pd.to_numeric(df['price'])
        df['month'] = pd.to_numeric(df['month'])
        df = df.sort_values(by=['price'])
        df.to_csv(f'output{date.today()}.csv', index=False)

        print(df.head(10))
        format_prices(df)
        sendemail.send_email()
        # new_dict = {id: [{'price': price}, {'year': year}, {'month', month}, {'day', day}] for id in range(len(date_price_database))}
        # driver.quit()

if __name__ == '__main__':
    get_flight_prices()
