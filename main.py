from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

import csv
import phonenumbers


from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import sys
import threading
import requests
from bs4 import BeautifulSoup

try:
    os.remove("Newfetched_links.csv")
except:
    pass


def fetchLinks(linktoScrape, scrapeStatus):
    group_links = []
    with open("groups_links.csv", "r", encoding="utf-8") as f:
        for i in csv.reader(f):
            if i != []:
                group_links.append(i[0])
    scrapeStatus.setText("Scrapping...")
    total_scraped=0
    if "category" in linktoScrape:

        r = requests.get(linktoScrape)
        mainContent = BeautifulSoup(r.text, "html.parser")
        try:
            pages = mainContent.find_all("a", "page-numbers")
            page = int(pages[len(pages) - 2].get_text().lower().replace("page",""))
        except:
            page=1
            
        print("total pages:",page)
        for i in range(1, page + 1):
            if linktoScrape[len(linktoScrape) - 1] == "/":
                r = requests.get(f"{linktoScrape}page/{i}/")
            else:
                r = requests.get(f"{linktoScrape}/page/{i}/")

            mainContent = BeautifulSoup(r.text, "html.parser")
            groups_pages = mainContent.find_all("h2", "entry-title")
            for page in groups_pages:
                try:
                    print("Checking for page ", page.find("a")["href"])
                    r2 = requests.get(page.find("a")["href"])
                    pageContent = BeautifulSoup(r2.text, "html.parser")
                    uls = pageContent.find_all("ul")
                    for ul in uls:
                        try:

                            for li in ul.find_all("li"):

                                 if("chat.whatsapp" in li.find("a")['href'] and li.find("a")['href'] not in group_links ):
                                    total_scraped+=1
                                    print(li.find("a")['href'], "-Scraped")
                                    
                                    with open(
                                        "groups_links.csv",
                                        "a",
                                        encoding="utf-8",
                                        newline="",
                                    ) as f:
                                        csv.writer(f).writerow(li.find("a")['href'])
                                    with open(
                                        "Newfetched_links.csv",
                                        "a",
                                        encoding="utf-8",
                                        newline="",
                                    ) as f:
                                        csv.writer(f).writerow(li.find("a")['href'])

                        except Exception as err:
                            print(err)
                            pass
                except:
                    pass
    else:

        r = requests.get(linktoScrape)
        mainContent = BeautifulSoup(r.text, "html.parser")
        groups_pages = mainContent.find_all("h2", "entry-title")
        links = mainContent.find_all("a")
        for link in links:
            try:
                if "chat.whatsapp" in link["href"] and link["href"] not in group_links:
                    total_scraped+=1
                    
                    print(link["href"], "-Scraped")
                    with open(
                        "groups_links.csv", "a", encoding="utf-8", newline=""
                    ) as f:
                        csv.writer(f).writerow([link["href"]])
                    with open(
                        "Newfetched_links.csv", "a", encoding="utf-8", newline=""
                    ) as f:
                        csv.writer(f).writerow([link["href"]])
            except:
                pass
    scrapeStatus.setText(f"Done Scraping. Scraped {total_scraped}.")
    

def get_country_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country_name = phonenumbers.region_code_for_number(parsed_number)
        country_code = parsed_number.country_code
        return country_name, country_code
    except phonenumbers.NumberParseException:
        print(f"Invalid phone number: {phone_number}")
        return None, None


def login_whatsappBot():

    chrome_options = webdriver.ChromeOptions()

    # Specify the directory where you want to save Chrome user data
    chrome_options.add_argument(f"--user-data-dir={os.getcwd()}//wp")

    # Disable logging for Chrome WebDriver
    chrome_options.add_argument("--log-level=3")  # 3 corresponds to the WARNING level

    # Create a WebDriver instance with the specified options
    # Initialize the Chrome driver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com/")
    input("Press Any Key after Login")
    driver.quit()


def start_whatsappBot(start, end, botStatus):
    group_links = []
    with open("groups_links.csv", "r", encoding="utf-8") as f:
        for i in csv.reader(f):
            if i != []:
                group_links.append(i[0])

    chrome_options = webdriver.ChromeOptions()

    # Specify the directory where you want to save Chrome user data
    chrome_options.add_argument(f"--user-data-dir={os.getcwd()}//wp")

    # Disable logging for Chrome WebDriver
    chrome_options.add_argument("--log-level=3")  # 3 corresponds to the WARNING level

    # Create a WebDriver instance with the specified options
    # Initialize the Chrome driver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com/")

    # Now, every time you launch Chrome using this driver instance, it will use the specified user data directory
    while (
        "WhatsApp Web".lower()
        not in driver.find_element(By.TAG_NAME, "body").text.lower()
    ):
        pass
    botStatus.setText("Bot is Working...")

    for index, gplink in enumerate(group_links[start : end + 1]):
        try:
            # Example: Opening a website
            print(index + start, "- Checking Group ", gplink)

            print("Joining Group")

            elem = driver.execute_script(
                'return document.querySelector("#side > div._3gYev > div > div._1EUay > div._2vDPL > div > div.to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt.qh0vvdkp")'
            )
            elem.send_keys(Keys.CONTROL, "a")
            elem.send_keys(Keys.BACKSPACE)

            time.sleep(1)
            elem.send_keys("bot-testing-links105")
            time.sleep(2)
            elem = driver.execute_script(
                """return document.querySelectorAll('[role="listitem"]')"""
            )
            for e in elem:
                e.click()
            time.sleep(2)
            elem = driver.execute_script(
                'return document.querySelector("#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._3Uu1_ > div > div.to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt")'
            )
            elem.send_keys(gplink)
            time.sleep(1)
            elem.send_keys(Keys.ENTER)
            time.sleep(1)
            driver.execute_script(
                """document.querySelectorAll('[title="View group"]')[document.querySelectorAll('[title="View group"]').length-1].click() """
            )
            time.sleep(1)
            driver.execute_script(
                """document.querySelector('[aria-disabled="false"]').click()"""
            )
            time.sleep(5)
            elem = driver.execute_script(
                'return document.querySelector("#main > header > div._2au8k")'
            )
            elem.click()
            time.sleep(1)
            btns = driver.execute_script(
                """return document.querySelectorAll('[role="button"]')"""
            )
            for btn in btns:
                if "View all".lower() in btn.text.lower():
                    btn.click()
                    break

            time.sleep(1)

            btns = driver.execute_script(
                """return document.querySelectorAll('[role="button"]')"""
            )
            for btn in btns:
                if "members".lower() in btn.text.lower():
                    nstr = ""
                    for char in btn.text.lower():
                        if char in "1234567890":
                            nstr += char

                    break
            total_member = int(nstr)
            print("total members ", total_member)
            print("Scraping phone numbers...")
            all_numbers = []
            i = 0
            while len(all_numbers) < total_member - 20:

                element = driver.execute_script(
                    f"""return document.querySelector("#app > div > span:nth-child(3) > div > span > div > div > div > div > div > div > div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp")"""
                )
                for span in element.find_elements(By.TAG_NAME, "span"):
                    try:
                        if "+" == span.text.strip()[0]:
                            if span.text.strip() not in all_numbers:
                                all_numbers.append(span.text.strip())
                    except:
                        pass

                driver.execute_script(
                    f"""document.querySelector("#app > div > span:nth-child(3) > div > span > div > div > div > div > div > div > div.g0rxnol2.g0rxnol2.thghmljt.p357zi0d.rjo8vgbg.ggj6brxn.f8m0rgwh.gfz4du6o.ag5g9lrv.bs7a17vp").scrollTo(0,{i})"""
                )

                if i > 200000:
                    break
                i += 1000
            if not os.path.exists("Country Wise"):
                os.mkdir("Country Wise")
            for number in all_numbers:
                try:
                    country_name, country_code = get_country_info(number)

                    with open(
                        f"Country Wise/{country_name}.csv",
                        "a",
                        encoding="utf-8",
                        newline="",
                    ) as f:
                        csv.writer(f).writerow([number])
                    with open(
                        "Extracted Phone Numbers.csv", "a", encoding="utf-8", newline=""
                    ) as f:
                        csv.writer(f).writerow([number])
                except Exception as err:
                    print(err)
            print("Done Scraping Group total = ", len(all_numbers))
            print("Leaving and Deleting Group")
            time.sleep(1)
            driver.execute_script(
                """document.querySelectorAll('[aria-label="Close"]')[0].click()"""
            )
            time.sleep(2)
            btns = driver.execute_script(
                """return document.querySelectorAll('[role="button"]')"""
            )
            for btn in btns:
                if "Exit group".lower() in btn.text.lower():
                    btn.click()
                    break
            time.sleep(1)
            btns = driver.find_elements(By.TAG_NAME, "button")
            for btn in btns:
                if "Exit group".lower() in btn.text.lower():
                    btn.click()
                    break
            time.sleep(3)
            btns = driver.execute_script(
                """return document.querySelectorAll('[role="button"]')"""
            )
            for btn in btns:
                if "Delete group".lower() in btn.text.lower():
                    btn.click()
                    break
            time.sleep(1)
            btns = driver.find_elements(By.TAG_NAME, "button")
            for btn in btns:
                if "Delete group".lower() in btn.text.lower():
                    btn.click()
                    break
            time.sleep(1)
            btns = driver.execute_script(
                """return document.querySelectorAll('[aria-label="Close"]')"""
            )
            for btn in btns:
                btn.click()
                time.sleep(1)
            time.sleep(3)
        except:
            print("Error on this Group")
            try:
                btns = driver.find_elements(By.TAG_NAME, "button")
                for btn in btns:
                    if "cancel".lower() in btn.text.lower():
                        btn.click()
                        break
            except:
                pass
            time.sleep(1)
            pass
            # Close the browser window
    driver.quit()
    botStatus.setText("Done..")


class whatsBot(QDialog):
    def __init__(self):
        super(whatsBot, self).__init__()
        loadUi("main.ui", self)
        self.doLogin.clicked.connect(self.LoginStart)
        self.startBot.clicked.connect(self.startbot_)
        self.startScraping.clicked.connect(self.startScraper)

    def LoginStart(self):
        t = threading.Thread(target=lambda: login_whatsappBot())
        t.daemon = True
        t.start()

    def startbot_(self):
        t = threading.Thread(
            target=lambda: start_whatsappBot(
                int(self.botStart.text()), int(self.botEnd.text()), self.botStatus
            )
        )
        t.daemon = True
        t.start()

    def startScraper(self):
        t = threading.Thread(
            target=lambda: fetchLinks(self.groupFetcherLink.text(), self.scrapingStatus)
        )
        t.daemon = True
        t.start()


##-------->
if __name__ == "__main__":
    app = QApplication(sys.argv)
    whatsBot = whatsBot()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(whatsBot)
    widget.setFixedWidth(391)
    widget.setFixedHeight(211)
    widget.setWindowIcon(QIcon("mail.ico"))
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("exiting")
