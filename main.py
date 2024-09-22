import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import json

CATEGORY = "environment"
URL = F"https://vtdigger.org/{CATEGORY}/"
ARTICLES_COUNT = 50

options = Options()
driver = webdriver.Chrome(options=options)

def get_images(output_dict):
  for i in range(len(output_dict)):
    page_res = requests.get(output_dict[i]["article_link"])
    soup = BeautifulSoup(page_res.content, 'lxml')
    content = soup.select('.entry-content > p')
    description = ""
    for p in content:
      description = description + p.text + " "
    images_links = soup.find_all("img")
    images = []
    for img in images_links:
      img_src = img.get("src")
      if(("facebook" not in img_src) and ("vtdigger.org" in img_src) and ("Logo" not in img_src)):
        images.append(img_src)
    output_dict[i]["description"] = description
    output_dict[i]["images"] = images
  
  output_file = 'output.json'

  with open(output_file, 'w',encoding='utf-8') as json_file:
        json.dump(output_dict, json_file, ensure_ascii=False, indent=4)

def get_info(driver):
  output = []
  buttons = driver.find_elements(By.TAG_NAME,"button")
  articles = driver.find_elements(By.TAG_NAME,"article")
  while(True):
    for button in buttons:
      if("Load more" in button.text):
        button.click()
        time.sleep(7)
    articles = driver.find_elements(By.TAG_NAME,"article")
    if(len(articles) >= ARTICLES_COUNT):
      break
  for article in articles[:ARTICLES_COUNT]:
      div_tag = article.find_element(By.CLASS_NAME,"entry-wrapper")
      title_tag = div_tag.find_element(By.TAG_NAME,"h2")
      title = title_tag.text
      summary = div_tag.find_element(By.TAG_NAME,"p").text
      article_link = title_tag.find_element(By.TAG_NAME,"a").get_attribute("href")
      date_tag = div_tag.find_element(By.CLASS_NAME,"entry-meta")
      date = date_tag.find_element(By.TAG_NAME,"time").text
      author = date_tag.find_element(By.CLASS_NAME,"byline").text
      entry = {"title":title,
               "summary":summary,
               "date":date,
               "author":author,
               "article_link":article_link}
      
      print(title)
      print(date)
      print(article_link)
      print("")
      output.append(entry)
  print(len(articles))
  return output


def make_request():
  driver.get(URL)
  time.sleep(7)
  output_dict = get_info(driver)
  get_images(output_dict)

make_request()