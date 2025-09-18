import time
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chromium.service import ChromiumService
from selenium import webdriver
from selenium.webdriver import Keys, ChromeOptions
from selenium.webdriver.common.by import By

service = ChromiumService("/usr/bin/chromedriver")

singer="adele"
wordlist="wr.txt"

settings=ChromeOptions()
settings.add_argument("--window-size=1920,1080")
settings.add_argument("--headless")
driver = webdriver.Chrome(options=settings,service=service)

driver.get("https://www.azlyrics.com/")

searchForm = driver.find_element(By.CLASS_NAME,"search")
searchForm.find_element(By.TAG_NAME,"input").send_keys(singer)
searchForm.find_element(By.TAG_NAME,"button").click()
#singerURL = driver.find_element(By.PARTIAL_LINK_TEXT, singer)
#singers=driver.find_elements(By.CLASS_NAME,"panel")[1]
time.sleep(1)
driver.print_page()
singerURL = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.azlyrics.com/a/"+singer+".html')]")

#gets list of songs from url
listOfSongs = BeautifulSoup(requests.get(singerURL.get_attribute("href")).text,"html.parser")
SongLinks=listOfSongs.find_all("a",href=lambda h: h and "/lyrics/"+singer+"/" in h)
#closes driver because it is no longer needed
driver.close()


for link in SongLinks:
    URL = "https://www.azlyrics.com"+link["href"]
    print(URL)
    lyricsBS = BeautifulSoup(requests.get(URL).text, "html.parser")
    lyrics=lyricsBS.find_all(
        lambda tag: tag.name == "div" and tag.get("class") is None and tag.get("id") is None)
    #removes unwanted text
    lyricsParsed=str(lyrics[0]).replace("<br/>","").replace('</div>, <div><img alt="Adele - 19 album cover" class="album-image" src="/images/albums/677/e2973539e72f35e57ae2e3a684d62a64.jpg"/></div>',"").replace("</div>","").replace("<div>","").replace("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->","")
    #time.sleep(5)
    print(lyricsParsed)

    with open(wordlist,"w") as f:
        f.write(lyricsParsed)
