
import time
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
from urllib.request import Request, urlopen
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.parse import CoreNLPParser
import openai
from selenium import webdriver
import google.generativeai as genai
import os

sheet_dict = {"P4": "NA", "P5": "NA", "P6": "NA", "P7": "NA", "P8": "NA", "P9": "NA", "P10": "NA", "P11": "NA", "P12": "NA", "P13": "NA", "P14": "NA", "P15": "NA", "P16": "NA", "P17": "NA", "P18": "NA", "P19": "NA", "P20": "NA", "P21": "NA", "P22": "NA", "P23": "NA", "P24": "NA", "P25": "NA", "P26": "NA", "P27": "NA", "P28": "NA"}


def generate_response(message):
    genai.configure(api_key="AIzaSyA_sgzhtdIkndjyWjz2lG94qIBbXpl8-og")
    #AIzaSyBs87q7ha7MLKjaixwdseAPZo2iKe0I0hc
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(message)
    return response.text

import cfscrape
def anti_bot_scraping(target_url):
    scraper = cfscrape.create_scraper()
    html_text = scraper.get(target_url,verify=False).text
    parsed_html = BeautifulSoup(html_text, 'html.parser')
    return parsed_html
def main():
    workbook = openpyxl.load_workbook('Competitor.xlsx')
    sheet = workbook.active
    url = "https://www.zara.com/uk/en/help-center/DeliveryMethods"
    soup= anti_bot_scraping(url)
    data= soup.find_all("div",class_="help-detail-main-layout-std__article")
    worr=soup.find_all('div',class_="help-detail-sections__article")
    word=" in two or three words from the below paragraph "
    print(worr)
    Standard_Delivery(data,word)
    time.sleep(60)
    nextday_delivery(worr,word)
    time.sleep(60)
    Click_Collect(worr,word)
    print(sheet_dict)

def Standard_Delivery(data,word):
    question="In how many days will the standard home delivery done " +word +data[0].text
    question2="How much is the cost for standard home delivery "+word+data[0].text
    question3="How much is the threshold cost for free delivery "+word+data[0].text
    question4= "What is the free threshold for health and beauty members"+word+data[0].text
    question5="What is the location and cost for quick delivery"+word +data[0].text
    message=generate_response(question)
    message1=generate_response(question2)
    message2=generate_response(question3)
    time.sleep(60)
    sheet_dict["P4"]=message
    sheet_dict["P5"]=message1
    sheet_dict["P6"]=message2
    print(sheet_dict["P4"])
    print(sheet_dict["P5"])
    print(sheet_dict["P6"])

def nextday_delivery(data,word):
    question="What is the next day delivery cost"+word+data[1].text
    question1="What is the next day delivery cut off time"+word+data[1].text
    question2="What is the same day delivery cost and cut off time "+word+data[1].text
    message=generate_response(question)
    message1=generate_response(question1)
    time.sleep(60)
    sheet_dict["P12"]=generate_response(question2)
    sheet_dict["P7"]=message
    sheet_dict["P8"]=message1
    print(message)
    print(message1)
    
    
def Click_Collect(data,word):
    question="When can I pick up earliest from the store"+word+data[0].text
    question1="How much is the pick up cost"+word+ data[0].text
    question2="How much is the free pickup threshold"+word+ data[2].text
    message=generate_response(question)
    message1=generate_response(question1)
    message2=generate_response(question2)
    sheet_dict["P14"]=message
    sheet_dict["P15"]=message1
    sheet_dict["P16"]=message2
    

main()
print(sheet_dict)
workbook = openpyxl.load_workbook('Competitor.xlsx')
sheet = workbook.active
for cell, value in sheet_dict.items():
    sheet[cell] = value
workbook.save('Competitor.xlsx')

workbook.close()