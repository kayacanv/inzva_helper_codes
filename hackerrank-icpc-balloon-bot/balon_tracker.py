import os
from string import ascii_lowercase
from random import choice
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

#1096527341 with kayacan
#906423021 with Havva
#-403396957 Balon info
bot_chatID = ["-403396957","",""]
def telegram_bot_sendtext(bot_message):
    bot_token = ''
    for ids in bot_chatID:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + ids + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
    return response.json()

class Downloader:
    printed = set()
    problems = []
    problems_color = {}
    def __init__(self):
        self.site = "https://www.hackerrank.com/"
#        driver_path = "/home/kayacan/Downloads/selenium/chromedriver"
#        browser = webdriver.Chrome(executable_path=driver_path)

        self.browser = webdriver.Chrome(executable_path="/home/kayacan/selenium/chromedriver")

        self.wait = WebDriverWait(self.browser, 10)

    def login(self, username, password):
        url = "https://www.hackerrank.com/auth/login?h_l=body_middle_left_button&h_r=login"
        self.browser.get(url)

        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='username']")))

        username_input = self.browser.find_element_by_xpath("//input[@name='username']")
        username_input.send_keys(username)

        password_input = self.browser.find_element_by_xpath("//input[@name='password']")
        password_input.send_keys(password)

        button = self.browser.find_element_by_xpath("//button[@data-analytics='LoginPassword']")
        button.click()

    def crawl(self, url):
        self.browser.get(url)
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//header[@class='submissions_list-header']")))

        source = self.browser.page_source

        soup = BeautifulSoup(source, "html.parser")
        rows = soup.findAll("div", {"class": "judge-submissions-list-view"})
        for row in rows:

            if "Accepted" in row.text: ## May Have Bug when Problem has  "accepted" as a substring
                names = row.findAll("a", {"class": "challenge-slug backbone"})
                # names[0].text = Problem Name , names[1].text = User name
                name = (names[0].text , names[1].text)
                if name in self.printed:
                    continue
                telegram_bot_sendtext("Username:"+name[1] + "\n Problem Name: "+name[0] + "\n Balon Color:"+self.problems_color[name[0]])
                print("Username:",name[1] , " Problem Name: ",name[0] , " Balon Color:",self.problems_color[name[0]])
                print("")
                self.printed.add(name)

    def get_problem_names(self, url):
        while True:
            try:
                self.browser.get(url)
                self.wait.until(ec.visibility_of_element_located((By.XPATH, "//div[@class='challenges-list']")))
                break
            except:
                print("ERROR ON get_problem_name: ", url)
                pass

        source = self.browser.page_source

        soup = BeautifulSoup(source, "html.parser")
        rows = soup.findAll("h4", {"class": "challengecard-title"})
        for a in rows:
            prob_name=a.find("a", {"class": "backbone"}).text
            print(prob_name)
            self.problems.append(prob_name)
    def track_balon(self,contest_link):
        url ="https://www.hackerrank.com/contests/" + contest_link + "/judge/submissions/{}".format(1)
        url_problem_page = "https://www.hackerrank.com/contests/" + contest_link + "/challenges"

        while len(self.problems) == 0:
            self.get_problem_names(url_problem_page)
        print (self.problems)
        for prob in self.problems:
            rengi = ""
            while True:
                rengi = input("\"" +prob + "\" Bu problem icin Balon rengi ver: ")
                if rengi not in self.problems_color:
                    break
            self.problems_color[prob] = rengi
        while True:
            self.crawl(url)
    @staticmethod
    def random_str(num=6):
        return "".join([choice(ascii_lowercase) for i in range(num)])





if __name__ == "__main__":
    telegram_bot_sendtext("HELLO!!")
    downloader = Downloader()
    contest_link = "inzva-algorithm-program-2019-2020-final" ## example format: "inzva-algorithm-program-2019-2020-final"
    telegram_bot_sendtext("Welcome to the balon info bot of "+contest_link)
    downloader.login("USER", "PASS")
    downloader.track_balon(contest_link)
