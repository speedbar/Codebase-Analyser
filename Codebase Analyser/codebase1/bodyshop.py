import html
import time
import openai
import openpyxl
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from openai import OpenAI
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import google.generativeai as genai
import os

sheet_dict = {"S4": "NA", "S5": "NA", "S6": "NA", "S7": "NA", "S8": "NA", "S9": "NA", "S10": "NA", "S11": "NA", "S12": "NA", "S13": "NA", "S14": "NA", "S15": "NA", "S16": "NA", "S17": "NA", "S18": "NA", "S19": "NA", "S20": "NA", "S21": "NA", "S22": "NA", "S23": "NA", "S24": "NA", "S25": "NA", "S26": "NA", "S27": "NA", "S28": "NA"}
workbook = openpyxl.load_workbook('Competitor.xlsx')
sheet = workbook.active
 
def generate_response(message):
    genai.configure(api_key="AIzaSyA_sgzhtdIkndjyWjz2lG94qIBbXpl8-og")
    #AIzaSyBs87q7ha7MLKjaixwdseAPZo2iKe0I0hc
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(message)
    return response.text
    
def main():
    url = "https://www.thebodyshop.com/en-gb/about-us/local-news/delivery-and-returns-information/i/i00001"
    session=requests.Session()
    page=session.get(url,verify=False)
    soup=BeautifulSoup(page.text,"html.parser")

    data=soup.find("div",class_="amp-dc-bambuser d-flex flex-column flex-wrap text-center ng-star-inserted")
    word="in one or two words from the below paragraph"
    data1=soup.find_all("div",class_="amp-dc-card-item__body-copy-1 amp-dc-card-item__body d-flex flex-column flex-grow-1 body-copy-margin ng-star-inserted")
    
    question= "What is the estimated standard delivery time"+word+ data.text
    sheet_dict["S4"]=generate_response(question)
    
    question1= "How much does the next day delivery costs"+word+ data.text
    sheet_dict["S7"]=generate_response(question1)
    time.sleep(60)
    
    question2= "At what price spend is the delivery free"+word+ data.text
    sheet_dict["S6"]=generate_response(question2)

    question3= "What is the cost for super saver delivery"+word+ data.text
    sheet_dict["S5"]=generate_response(question3)
    time.sleep(60) 

    question4= "Order before what time for express delivery"+word+ data.text
    sheet_dict["S8"]=generate_response(question4)
    
    question5= "In how much time we can collect from store"+word+ data1[1].find_all("p")[0].text
    sheet_dict["S14"]=generate_response(question5)

    question6= "What is the charge for collect in store"+word+ data.text
    sheet_dict["S15"]=generate_response(question6)
    # eg=generate_response(question)
    # print(eg)

main()
print(sheet_dict)
for cell, value in sheet_dict.items():
    sheet[cell] = value

workbook.save('Competitor.xlsx')
workbook.close()



