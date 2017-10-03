from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pass_detail(boarding_station,pass_list,phn_num):
    if boarding_station!=None:
        driver.find_element_by_id("addPassengerForm:boardingStation").send_keys(boarding_station)
    elem=driver.find_elements_by_css_selector("input[type='text']")
    count=0
    for passenger in pass_list:
        elem[count*3].send_keys(passenger['name'])
        elem[(count*3)+1].send_keys(passenger['age'])
        driver.find_elements_by_css_selector("option[value='M']")[count].find_element_by_xpath(".//ancestor::select").send_keys(passenger['gender'])
        driver.find_elements_by_css_selector("option[value='UB']")[count].find_element_by_xpath(".//ancestor::select").send_keys(passenger['pref'])
        count=count+1
    driver.find_element_by_id("addPassengerForm:autoUpgrade").click()
    driver.find_element_by_id("addPassengerForm:mobileNo").clear()
    driver.find_element_by_id("addPassengerForm:mobileNo").send_keys(phn_num)
    input("-----solve the captcha and then press enter------")
    driver.find_element_by_css_selector("input[value=' Next ']").click()
    

def journey_detail(from_station,to_station,travel_date):
    try:
        driver.find_element_by_id("jpform:fromStation").clear()
        driver.find_element_by_id("jpform:toStation").clear()
        driver.find_element_by_id("jpform:journeyDateInputDate").clear()
        driver.find_element_by_id("jpform:fromStation").send_keys(from_station)
        driver.find_element_by_id("jpform:toStation").send_keys(to_station)
        driver.find_element_by_id("jpform:journeyDateInputDate").send_keys(travel_date)
        driver.find_element_by_id("jpform:jpsubmit").click()        
    except Exception as e:
        print(e)

def check_ticket(bank_name):
    driver.find_element_by_id("NETBANKING").click()
    elem=driver.find_elements_by_id("NETBANKING")
    for bank in elem:
        if bank_name in bank.find_element_by_xpath("..").text:
            bank.click()
            break
    cont=input("########################################\n########################################\n########################################\nPlease Carefully check all details and press Y to continue\n########################################\n########################################\n########################################\nPlease Carefully check all details and press Y to continue :")
    if cont=='y' or cont=='Y':
        driver.find_element_by_css_selector("input[value='Make Payment']").click()
        return True
    else:
        return False


def irctc_login(user_id,password):
    try:
        driver.find_element_by_id("demon_container").find_element_by_tag_name("input").click()
    except:
        print("Notice iframe not present")
    try:
        captcha=None
        while captcha==None:
            driver.find_element_by_id("usernameId").clear()
            driver.find_element_by_class_name("loginPassword").clear()
            driver.find_element_by_id("usernameId").send_keys(user_id)
            driver.find_element_by_class_name("loginPassword").send_keys(password)
            captcha=input("enter captcha value: ")
            if captcha=="":
                captcha=None
                print("Captcha value should not be empty")
            else:
                driver.find_element_by_class_name("loginCaptcha").send_keys(captcha)
                driver.find_element_by_id("loginbutton").click()
                if "Invalid Captcha" in driver.page_source :
                    captcha=None
                    print("Wrong captcha value, enter again")
                    try:
                        driver.find_element_by_id("demon_container").find_element_by_tag_name("input").click()
                    except:
                        print("Notice iframe not present")
                    driver.find_element_by_id("loginerrorpanelok").click()
                if "Wrong credentials" in driver.page_source:
                    captcha=None
                    print("Wrong Credentials")
                    try:
                        driver.find_element_by_id("demon_container").find_element_by_tag_name("input").click()
                    except:
                        print("Notice iframe not present")
                    driver.find_element_by_id("loginerrorpanelok").click()
                    return True
        print("yipee login done")
    except Exception as e:
        print(e)
    return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("http://www.irctc.co.in")
    assert "Next" in driver.title
    user_id="*********"
    password="********"
    from_station="VASCO DA GAMA - VSG"
    to_station="GWALIOR - GWL"
    travel_date="12-05-2017"
    train_num='12779'
    journey_class='SL'
    bank_name='ICICI'
    bank_id=''
    bank_pass=''
#    atm_seq=[{'A':},{'B':},{'C':},{'D':},{'E':},{'F':},{'G':},{'H':},{'I':},{'J':},{'K':},{'L':},{'M':},{'N':},{'O':},{'P':}]
    #Add passenger list like below, Preference are "UPPER/MIDDLE/LOWER/SIDE UPPER/SIDE LOWER" and gender are "Male/Female" Use exact spelling as written here they are case sensitive
    pass_list=[{'name':'Vinay Singh','age':'27','gender':'Male','pref':'UPPER'}]
    boarding_station='PUNE JN - PUNE'
    phn_num='7276911795'
    while irctc_login(user_id,password):
        user_id=input("Enter name: ")
        password=input("Enter Password: ")
    journey_detail(from_station,to_station,travel_date)
    tatkal=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='TQ']")))
    tatkal.click()
    driver.find_element_by_link_text(train_num).find_element_by_xpath(".//ancestor::tr").find_element_by_link_text(journey_class).click()
    book_now=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Book Now")))
    book_now.click()
    pass_detail(boarding_station,pass_list,phn_num)
    if check_ticket(bank_name):
        cont=input("you are on bank site, do you wish to perform manually from here? press y to perform manually :")
        if cont!='y' or cont!='Y':
            print("will code later")
    else:        
        driver.quit()









