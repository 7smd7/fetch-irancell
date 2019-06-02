# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time
import khayyam
import numpy as np

ip = "46.209.199.156"
port = 808
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", ip)
profile.set_preference("network.proxy.http_port", port)
profile.set_preference("network.proxy.ssl", ip)
profile.set_preference("network.proxy.ssl_port", port)
profile.set_preference("network.proxy.ftp", ip)
profile.set_preference("network.proxy.ftp_port", port)

profile.update_preferences()
# driver = webdriver.Firefox(profile)
driver = webdriver.Firefox()

user="??"
password="??"

Loged_In = False
int
dict = {}

class Customer :
    def __init__(self,dataused,datamax,leftover):
        self.dataused = dataused
        self.datamax = datamax
        self.leftover = leftover

def login(user, password):
    print ('Loging in. . .')
    driverr = driver
    driverr.get("https://my.irancell.ir/")
    driverr.find_element_by_id("inputFieldMSISDN").click()
    driverr.find_element_by_id("inputFieldMSISDN").clear()
    driverr.find_element_by_id("inputFieldMSISDN").send_keys(user)
    driverr.find_element_by_id("verifyButton").click()
    time.sleep(2)
    driverr.find_element_by_id("verifyEcarePass").click()
    driverr.find_element_by_id("inputFieldPassword").click()
    driverr.find_element_by_id("inputFieldPassword").clear()
    driverr.find_element_by_id("inputFieldPassword").send_keys(password)
    driverr.find_element_by_id("verifyEcareButton").click()
    time.sleep(3)
    global Loged_In
    Loged_In = True
    print ('loged in successfuly')

def check_alluser():
    if not Loged_In:
        login(user,password)
    global dict
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(3)
    i=0
    print ("MSISDN \t\tUsedData \tMax \tAvailable")
    try:
        while (driver.find_element_by_xpath(u"//a[contains(@href, '#consumer%s')]" % (i)).is_enabled()): #is_displayed()):
            driver.find_element_by_xpath(u"//a[contains(@href, '#consumer%s')]" % (i)).click()
            time.sleep(3)
            datamax = driver.find_element_by_id("datamax%s" % (i)).text
            dataused = int(driver.find_element_by_id("dataused%s" % (i)).text)
            MSISDN = int(driver.find_element_by_xpath("(//div[@id='sharedboltondata']/h4)[%s]" % (i+3)).text)
            if (datamax.isdigit()):
                datamax=int(datamax)
                if(datamax<21000 and datamax>0):
                    print("%d \t %d \t %d \t %d" %(MSISDN, dataused, datamax, datamax-dataused))
                    dict[MSISDN]=Customer(dataused,datamax,datamax-dataused)
                elif (datamax<= 0):
                    print("%d \t %d \t %d \t %d" %(MSISDN, dataused, datamax, 0))
                    dict[MSISDN]=Customer(dataused,datamax,0)
                else:
                    print("%d \tno Limit" %MSISDN)
                    dict[MSISDN]=Customer(dataused,datamax,-1)
            else:
                print("%d no Limit" %MSISDN)
                dict[MSISDN]=Customer(dataused,datamax,-1)
            i+=1
            time.sleep(1)
    except:
        pass

    save()

def check_self():
    if not Loged_In:
        login(user,password)
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(4)
    driver.find_element_by_link_text(u"مشاهده جزئیات").click()
    time.sleep(2)
    expiryTime = driver.find_element_by_id("expiryValData").text
    dataSelf = driver.find_element_by_id("dataVal").text
    today = {"mounth" : int(str(khayyam.JalaliDatetime.now())[5:7]),
             "day" : int(str(khayyam.JalaliDatetime.now())[8:10])}
    expiryDate={"mounth" : int(expiryTime[5:7]),
                "day" : int(expiryTime[8:10])}
    if ((today["mounth"]==expiryDate["mounth"] and expiryDate["day"]-today["day"] in range(0,2))
        or ("مگابایت" in dataSelf)):
        check_alluser()
        buy()
        changelimitforall()
        driver.get("https://my.irancell.ir/sharedaccounts")
        time.sleep(4)
        dataSelf = driver.find_element_by_id("dataVal").text
        if "مگابایت" in dataSelf:
            print("the buy wasn't seccessfull, so try manually")


def changelimit(number,limit):
    if not Loged_In:
        login(user,password)
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(3)
    i=0
    try:
        while (driver.find_element_by_xpath(u"//a[contains(@href, '#consumer%s')]" % (i)).is_displayed()):
            MSISDN = int(driver.find_element_by_xpath("(//div[@id='sharedboltondata']/h4)[%s]" % (i+3)).text)
            if (MSISDN==number):
                driver.find_element_by_xpath(u"//a[contains(@href, '#consumer%s')]" % (i)).click()
                time.sleep(2)
                driver.find_element_by_xpath("(//img[@id='editImage2'])[%s]" % (i+1)).click()
                time.sleep(2)
                if (limit==-1):
                    driver.find_element_by_id("unlimited").click()
                    time.sleep(2)
                else:
                    driver.find_element_by_id("rangebutton1").send_keys(limit)
                driver.find_element_by_id("AddButton2").click()
                time.sleep(3)
                result = driver.find_element_by_id("modalBodyMessage1").text
                print("%d %s"%(MSISDN,result))
                break
            i+=1
    except:
        pass

def changelimitforall():
    global dict
    for item in dict.keys():
        if(dict[item].leftover==-1):
            print("%d was unlimited" %item)
        else:
            changelimit(item,dict[item].leftover)

def buy():
    if not Loged_In:
        login(user,password)
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(3)
    driver.find_element_by_link_text(u"خرید").click()
    time.sleep(3)
    driver.find_element_by_xpath("(//button[@id='buyNowButton'])[5]").click()
    time.sleep(3)
    driver.find_element_by_id("PrimaryAction2Button").click()
    time.sleep(3)
    driver.find_element_by_id("PrimaryAction2Button").click()
    time.sleep(10)
    result = driver.find_element_by_id("modalBodyMessage1").text
    print(result)


def add_user(MSISDN):
    if not Loged_In:
        login(user,password)
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(3)
    driver.find_element_by_id("addimage").click()
    time.sleep(3)
    driver.find_element_by_id("newConsumer").send_keys(MSISDN)
    driver.find_element_by_id("AddButton").click()
    time.sleep(3)
    result = driver.find_element_by_id("modalBodyMessage1").text
    print(result)

def delete_user(MSISDN):
    if not Loged_In:
        login(user,password)
    driver.get("https://my.irancell.ir/sharedaccounts")
    time.sleep(3)
    driver.find_element_by_xpath("//img[@onclick='javascript:deleteCustomer(\"%d\",\"9372588349\")']"%MSISDN).click()
    time.sleep(3)
    result = driver.find_element_by_id("modalBodyMessage1").text
    print(result)
#-------------------------------------------------------------------------#
def save():
    global dict
    a = np.array(dict)
    np.save('export',a)
    stamp = time.localtime(time.time())       #    (time.ctime(time.time()))
    stamp = str(stamp[:5]).replace('(','').replace(',','-').replace(' ','').replace(')','')
    np.save(stamp,a)

def load():
    global dict
    a = np.load('export.npy')
    dict = np.ndarray.tolist(a)

# def load(date):
#     global dict
#     a = np.load('%s.npy' % date)
#     dict = np.ndarray.tolist(a)

def validate_Update():
    load()
    global dict
    userLimit = dict
    check_alluser()
    load()
    validated = True
    for item in userLimit.keys():
        if userLimit[item].leftover != dict[item].datamax:
            validated = False
            break
    if not validated:
        dict = userLimit
        a = np.array(dict)
        np.save('export',a)
        changelimitforall()
        validate_Update()

def showdf():
    # load()
    global dict
    userLimit = dict
    print ("Checking Users!")
    check_alluser()
    dc = True
    for item in userLimit.keys():
        if userLimit[item].leftover != dict[item].datamax:
            print  ("%s \t %s" %(item,userLimit[item].leftover-dict[item].datamax))
            dc = False
    if dc:
        print ("Everithing is ok :-)")

def check_balance():
    load()
    global dict
    Sold = 0
    for item in dict.keys():
        if dict[item].leftover < 20480:
            Sold = Sold + dict[item].leftover
    balance = 20480 - Sold
    print ('Balance: ',balance)
    return balance

def PrintLog():
    load()
    print ("MSISDN \t UsedData \t Max \t Available")

    for item in dict.keys():
        print  ("%d \t %d \t %d \t %d" %(int(item), int(dict[item].dataused), int(dict[item].datamax), int(dict[item].leftover)))

login(user,password)
msg = "1- Check All User \n2- Change Limit For All\n3- Print Log \n4- Check Root Balance \n0- Exit \nselect action: "
while True:
    print ("-------------------------------------------")
    inp = input(msg)
    print ("-------------------------------------------")
    if inp == 0 :
        break
    elif inp == 1:
        check_alluser()
    elif inp == 2:
        load()
        changelimitforall()
    elif inp == 3:
        PrintLog()
    elif inp == 4:
        check_balance()



# def PrintLog(date):
#     load(date)
#     print "MSISDN \t UsedData \t Max \t Available"

#     for item in dict.keys():
#         print  "%d \t %d \t %d \t %d" %(int(item), int(dict[item].dataused), int(dict[item].datamax), int(dict[item].leftover))


# changelimitforall()
# validate_Update()
# check_balance()
# PrintLog()

# def repeat():
#     """
#     repeat function till success!
#     """
#     try:
#         check_alluser()
#     except:
#         print 'retry!'
#         repeat()

# repeat()
# print "checking users log..."
# check_alluser()
# print "update limits..."
# load()
# changelimitforall()
# print "checking for validate!"
# showdf()
# a = time.localtime(time.time())       #    (time.ctime(time.time()))
# a = str(a[:5]).replace('(','').replace(',','-').replace(' ','').replace(')','')
# print a

# PrintLog(a)
# PrintLog()
