from selenium import webdriver
from time import sleep
from openpyexcel import *
import smtplib
from email.message import EmailMessage

from selenium.webdriver.chrome.options import Options

opt=Options()
opt.add_argument("--headless")  #Open Flipkart in background
driver=webdriver.Chrome(executable_path="C:\selenium\chromedriver_win32\chromedriver.exe", options=opt)

driver.maximize_window()
driver.get("https://www.flipkart.com/")
driver.implicitly_wait(10)
driver.find_element_by_xpath("/html/body/div[2]/div/div/button").click()
sleep(3)
driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input").send_keys("iphone")
sleep(2)
driver.find_element_by_xpath("//html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/button").click()
sleep(7)
devices=driver.find_elements_by_class_name("s1Q9rs")
prices= driver.find_elements_by_class_name("_30jeq3")

mydevice=[]
myprice=[]

for device in devices:
    mydevice.append(device.text)

for price in prices:
    myprice.append(price.text)

final= zip(mydevice, myprice)

wb=Workbook()
wb['Sheet'].titl='Flipkart Data'
sh1=wb.active

sh1.append(['Name', 'Price'])
for x in list(final):
    sh1.append(x)

wb.save("FinalRecords.xlsx")

msg=EmailMessage()
msg['Subject']='iPhone Records'
msg['From']='Vinayak Rai'
msg['To']='#Sender Mail I'd'

with open('EmailTemplate.txt') as myfile:
    data=myfile.read()
    msg.set_content(data)

with open("FinalRecords.xlsx", "rb") as f:
    file_data=f.read()
    file_name=f.name
    msg.add_attachment(file_data, maintype="application", subtype="xlsx", filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login("# YourMail I'd", "#Password")
    server.send_message(msg)

print("Email sent!!")
