from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.common import alert
from collections import OrderedDict
import time
import json
import sys

# Set Firefox Settings
fp = webdriver.FirefoxProfile()
# fp.add_extension(extension='/Users/MickaelNg/Dropbox/Project - Udemy/firebug-2.0.18-fx.xpi')
# fp.add_extension(extension='/Users/MickaelNg/Dropbox/Project - Udemy/firepath-0.9.7.1-fx.xpi')
fp.set_preference("extensions.firebug.currentVersion", "2.0.18")  # Avoid startup screen
fp.set_preference("browser.tabs.remote.autostart", False)
fp.set_preference("browser.tabs.remote.autostart.2", False)

# Declare Variables
big_list_of_regnum = {}  # Big List Of All Registration Num
data = OrderedDict()  # Declare data for use as JSON container
list_records = []  # Declare page record list on page
# Registered Name
xpath_reg_name = "//*[@id='profDetails']/div[@class='table-head']"
# Registration Number
xpath_regnum = "//*[@class='no-border table-title' and starts-with(., 'Registration Number')]" \
               "/following-sibling::*"
# Practicing Cert Start Date
xpath_pcsd = "//*[@class='no-border table-title' and starts-with(., 'Practising Certificate Start Date')]" \
             "/following-sibling::*"
# Practicing Cert End Date
xpath_pced = "//*[@class='no-border table-title' and starts-with(., 'Practising Certificate End Date')]" \
             "/following-sibling::*"
# Qualifications
qualifications = ""
xpath_qualifications = "//*[@class='no-border table-title' and starts-with(., 'Qualifications')]/following-sibling::*"
xpath_profession = "//*[@class='table-title align-left' and starts-with(., 'Type of Register')]"  # Optom, Optician, ETC
# Registration Date
xpath_reg_date = "//*[@class='no-border table-title' and starts-with(., 'Registration Date')]" \
                 "/following-sibling::*"

# Registration Type Full, Provisional, Etc
xpath_reg_type = "//*[@class='no-border table-title' and starts-with(., 'Registration Type')]/following-sibling::*"

xpath_pri_practice_name = "//*[@class='table-title align-left' and starts-with(., 'Primary')]" \
                          "/following-sibling::div" \
                          "//td[@class='no-border table-title' and starts-with(.,'Name of Place of Practice')]" \
                          "/following-sibling::*"
xpath_pri_practice_addr = "//*[@class='table-title align-left' and starts-with(., 'Primary')]" \
                          "/following-sibling::div" \
                          "//td[@class='no-border table-title' and starts-with(.,'Address of Place of Practice')]" \
                          "/following-sibling::*"
xpath_sec_practices = "//*[@class='table-title align-left' and starts-with(., 'Secondary')]" \
                      "/following-sibling::table/tbody"


# load settings
def loadsettings(loadfile):
    in_file = open(loadfile, "r")
    global big_list_of_regnum
    big_list_of_regnum = json.load(in_file, object_pairs_hook=OrderedDict)
    in_file.close()


# save data
def savedata(prefix, dictvar):
    out_file = open(prefix+filename, "w")
    json.dump(dictvar, out_file, indent=4, separators=(',', ':'), sort_keys=False)
    out_file.close()


# Calc num of records ("view more details") on this page and store link in list_records
def create_list_records():
    while True:
        try:
            global list_records
            list_records = []  # Clear list_records
            xpath_list_records = "//a[text()='View more details']"
            element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, xpath_list_records)))
            list_records = driver.find_elements_by_xpath(xpath_list_records)
            xcounter = 0
            for x in list_records:
                # list records on page and convert to onclick commands
                list_records[xcounter] = list_records[xcounter].get_attribute("onclick").split(";")[0]
                xcounter += 1
            # for x in list_records:
            #     print x
            print "List Records Refreshed"
            # return len(list_records)
            break
        except exceptions.StaleElementReferenceException:
            print "too fast, chilling for 3s"
            time.sleep(3)
        except exceptions.NoSuchElementException:
            print "No Such Element"
            break


def extractdetails():
    loader = 0
    while loader < 10:  # Wait for page to load
        try:  # wait for load
            element = WebDriverWait(driver, 3).\
                until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Back to Search Results")))
            break
        except:
            print "waiting for load"
            loader += 1

    print "========================================================="
    print "Extracting %s %s" % (driver.find_element_by_xpath(xpath_reg_name).text,
                               driver.find_element_by_xpath(xpath_regnum).text)

    global qualifications
    qualifications = driver.find_element_by_xpath(xpath_qualifications).text

    # check if more then 1 qualification and split in to list
    if qualifications.find("\n") > 0:  # Check if more then 1 Qualifications
        qualifications = qualifications.split("\n")  # Split Into Individual Lines
        # print "q more then 1 so split"
    else:
        qualifications = [qualifications]
    # print qualifications
    # split individual qualifications into different sections
    counter = 0
    for qualification in qualifications:
        qualifications[counter] = qualifications[counter].split(",",2)  # split qualifications into sections
        # print "qcounter " + qualifications[counter][0]
        if qualifications[counter][0] == "Fellow":
            csetype = "Diploma"
            csename = qualifications[counter][0] + "," + qualifications[counter][1].rsplit(" ", 1)[0]
            cseyear = qualifications[counter][1].rsplit(" ", 1)[1]
            cseschool = qualifications[counter][2].split(",")[0].strip()
            csecountry = qualifications[counter][2].split(",")[1].strip()
        elif qualifications[counter][0] == "":
            csetype = "Unknown"
            csename = "Qualifications Not Shown"
            cseyear = csetype
            cseschool = csetype
            csecountry = csetype
        else:
            x = qualifications[counter][0].split(" ", 1)
            csetype = x[0]
            # print csetype
            csename = qualifications[counter][0].rsplit(" ", 1)[0]
            # print csename
            cseyear = qualifications[counter][0].rsplit(" ", 1)[1]
            # print cseyear
            cseschool = qualifications[counter][1].strip()
            # print cseschool
            if qualifications[counter][2].find(",") > 0:
                x = qualifications[counter][2].split(",")
                csecountry = x[-1].strip()
            else:
                csecountry = qualifications[counter][2].strip()

        if csename.find("Doctor of Optometry") != -1 or csename.find("O.D.") != -1:
            csetype = "OD"
        elif csename.find("Doctor of Philosophy") != -1:
            csetype = "PhD"
        elif csename.find("NITEC") != -1 or csename.find("Adv Cert") != -1 \
                or csename.find("Upg Prog") != -1 or csename.find("Opticianry") != -1 \
                or csename.find("CCO-Conv") != -1 or csename.find("Contact Lens Examination") != -1 \
                or csename.find("ADVANCE CERTIFICATE") != -1:
            csetype = "Certificate"
        elif csename.find("F.B.D.O") != -1 or csename.find("Diploma") != -1 \
                or csename.find("British College of Optometrists") != -1:
            csetype = "Diploma"
        elif csename.find("Qualifications Not Shown") != -1:
            csetype = "Unknown"
        else:
            pass

        qualifications[counter] = [csetype, csename, cseyear, cseschool, csecountry]
        counter += 1

    global pri_prac_name
    pri_prac_name = driver.find_element_by_xpath(xpath_pri_practice_name).text.strip()  # Pri Practice Name
    if pri_prac_name == "-":
        pri_prac_name = "No Primary Practice"
    else:
        pass

    print "Pri Practice: " + pri_prac_name

    global pri_prac_addr
    global pri_prac_postalcode
    if len(pri_prac_name) < 5 or pri_prac_name == "No Primary Practice":
        pri_prac_addr = ""
        pri_prac_postalcode = ""
    else:
        pri_prac_addr = driver.find_element_by_xpath(xpath_pri_practice_addr).text  # Pri Practice Address
        pri_prac_postalcode = driver.find_element_by_xpath(xpath_pri_practice_addr).text.split()[-1]  # PriPrac PostCode

    #Secondary Practice
    try:
        global sec_prac_list
        sec_prac_list = driver.find_elements_by_xpath(xpath_sec_practices)
    except exceptions.NoSuchElementException:
        print "No Secondary Practice"
    counter = 0
    for prac in sec_prac_list:  # set sec_prac_list and split lines
        sec_prac_list[counter] = sec_prac_list[counter].text.split("\n", 1)  # split line 2 practice name n practice add
        y = sec_prac_list[counter][1].split("\nTel")  # split add and save in external var
        sec_prac_list[counter].pop()  # remove practice add from list
        sec_prac_list[counter] = sec_prac_list[counter] + y  # combine practice name and add
        sec_prac_list[counter].pop()  # remove tel number and other useless text
        sec_prac_list[counter].append(sec_prac_list[counter][-1].rsplit(" ", 1)[1])  # append postal code
        sec_prac_list[counter][0] = sec_prac_list[counter][0][len("Name of Place of Practice") + 1:]  # clean up
        sec_prac_list[counter][1] = sec_prac_list[counter][1][len("Address of Place of Practice") + 1:]  # clean up
        # print sec_prac_list[counter]
        # sec_prac_list[counter].extend(x)
        # sec_prac_list[counter] = sec_prac_list[counter][:2]
        counter += 1
    print regnumkeys[currentkey]
    regnum = unicode(driver.find_element_by_xpath(xpath_regnum).text)
    #regnum = regnumkeys[currentkey]
    print regnum in regnumkeys
    # append details to registra

    #Adding Data ExtractDate
    ExtractDate = filename.rsplit("regnum",1)[1]
    ExtractDate = ExtractDate[:8]
    try:
        data[regnum].update({"ExtractDate":ExtractDate})
    except:
        data[regnum].update({"ExtractDate" : "-"})

    if data[regnum]["ExtractDate"] == "-":
        data[regnum].update({"ExtractYear" : "-"})
        data[regnum].update({"ExtractMth" : "-"})
        data[regnum].update({"ExtractDay" : "-"})
    else:
        data[regnum].update({"ExtractYear" : ExtractDate[:4]})
        data[regnum].update({"ExtractMth" : ExtractDate[4:6]})
        data[regnum].update({"ExtractDay" : ExtractDate[6:]})

    try:
        data[regnum].update({"Name":driver.find_element_by_xpath(xpath_reg_name).text})
    except:
        data[regnum].update({"Name":"-"})

    Profession = ""
    try:
        data[regnum].update({"Profession" : driver.find_element_by_xpath(xpath_profession).text.split(":")[1].strip()})
        Profession = driver.find_element_by_xpath(xpath_profession).text.split(":")[1].strip()
    except:
        data[regnum].update({"Profession": "" })
        Profession = ""

    if Profession.find("Optometrist") != -1:
        data[regnum].update({"ProfessionGroup" : "Optometrist"})
    elif Profession.find("Optician") != -1:
        data[regnum].update({"ProfessionGroup" : "Optician"})
    else:
        pass

    try:
        data[regnum].update({"Qualifications" : qualifications})
    except:
        data[regnum].update({"Qualifications": ""})

    try:
        # Practicing Cert Start Date DDMMYYYY from dd/mm/yyyy format
        data[regnum].update({"PCSD" : driver.find_element_by_xpath(xpath_pcsd).text.replace("/", "")})
    except:
        data[regnum].update({"PCSD": ""})

    try:
        # Practicing Cert End Date DDMMYYYY from dd/mm/yyyy format
        data[regnum].update({"PCED" : driver.find_element_by_xpath(xpath_pced).text.replace("/", "")})
    except:
        data[regnum].update({"PCED": ""})

    try:
        # Date of Registration DDMMYYYY from dd/mm/yyyy format
        data[regnum].update({"RegDate" : driver.find_element_by_xpath(xpath_reg_date).text.replace("/", "")})
    except:
        data[regnum].update({"RegDate": ""})

    try:
        element = driver.find_element_by_xpath(xpath_reg_type)
        data[regnum].update({"RegType" : driver.find_element_by_xpath(xpath_reg_type).text})
    except:
        data[regnum].update({"RegType": ""})

    data[regnum].update({"Primary Practice" : [
        pri_prac_name,  # Pri Practice Name
        pri_prac_addr,  # Pri Practice Address
        pri_prac_postalcode  # Pri Practice Postal Code
        ]})
    data[regnum].update({"Secondary Practice" : sec_prac_list})
    print "Extracted %s %s" % (driver.find_element_by_xpath(xpath_reg_name).text,
                               driver.find_element_by_xpath(xpath_regnum).text)

# Open Firefox, Go to URL, select Frame
# driver = webdriver.Firefox(firefox_profile=fp,executable_path='./geckodriver')
driver = webdriver.Firefox(firefox_profile=fp, executable_path='./geckodriver_0.28.0/geckodriver')
url = "http://prs.moh.gov.sg/prs/internet/profSearch/main.action?hpe=OOB"
driver.get(url)
driver.switch_to.frame("msg_main")

# CLICK "Search"
try:
    element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.NAME, "btnSearch")))
    element = driver.find_element_by_name("btnSearch")
    element.click()
    print "Clicked Search"
except exceptions.NoSuchElementException:
    print "No Such Element"

try:  # getting last page
    print "Getting last page"
    element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.LINK_TEXT, "Last")))
    global lastpage
    lastpage = element.get_attribute("href")
    lastpage = lastpage.rsplit("(", 1)[1]
    lastpage = int(lastpage[:-1])
    print "Last page " + str(lastpage)
except exceptions.NoSuchElementException:
    print "No Such Element"

# check for arguments if no arguments create reg list.
if len(sys.argv) < 2:
    filename = str(time.strftime("%Y%m%d-%H%M%S.json", time.localtime()))
else:
    filename = str(sys.argv[1])
    loadsettings(sys.argv[1])
    print filename.find("/")
    if filename.find("/") >= 0:
        filename = sys.argv[1].rsplit("/", 1)[1]  # split file name from path
        print filename
    else:
        print filename


if len(sys.argv) < 2:
    # Grab all regnumbers
    big_list_of_regnum = {}
    page = 1
    while page <= lastpage:
        try:
            # Wait for page to load
            loader = 0
            while loader < 10:
                try:  # wait for load
                    element = WebDriverWait(driver, 3)\
                        .until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "View more details")))
                    break
                except:
                    print "waiting for load"
                    loader += 1

            list_of_regnum = driver.find_elements_by_xpath("//td[@class='no-border font15px']")
            for x in list_of_regnum:
                big_list_of_regnum[x.text.split("(")[len(x.text.split("("))-1][:-1]] = {}
                print x.text
            # element = driver.find_element_by_link_text("Next")  # click next page
            # element.click()
            # element = ""  # refresh element

            print "[" + str(time.strftime("%Y%m%d-%H%M%S", time.localtime())) + "] " + "page " + str(page) + " done!"
            page += 1
            driver.execute_script("gotoPageDEFAULT(" + str(page) + ")")
            print "[" + str(time.strftime("%Y%m%d-%H%M%S", time.localtime())) + "] " + "going page " + str(page) + " of " + str(lastpage)
            print "========================================================="

            # Wait for page to load
            global nowpage
            nowpage = page - 1
            while nowpage < page:
                try:  # wait for load
                    xpath_current_page = "//label[@class ='pagination_selected_page']"
                    element = WebDriverWait(driver, 3)\
                        .until(EC.presence_of_element_located((By.XPATH, xpath_current_page)))
                    nowpage = int(driver.find_element_by_xpath(xpath_current_page).text)
                    time.sleep(1)
                except:
                    if nowpage == lastpage:
                        print "[" + str(time.strftime("%Y%m%d-%H%M%S", time.localtime())) + "] " + "lastpage reached"
                        savedata("regnum", big_list_of_regnum)
                        raise SystemExit
                    else:
                        print "waiting for load"
            print "Waiting 1s"
            savedata("regnum", big_list_of_regnum)
            time.sleep(1)

        except exceptions.NoSuchElementException:
            try:
                # all nav links(first, next, previous, last)
                list = driver.find_elements_by_xpath("//*[@class='text_right']/*[@class='pagination']")
                if len(list) == 2 and list[0].text == "First":  # Check if Last Page
                    print "Last Page Reached, Raise System Exit"
                    savedata("regnum", big_list_of_regnum)
                    raise SystemExit
                else:
                    print "Not Sure What Error but 'Next' Not Found"
                    savedata("regnum", big_list_of_regnum)
                    driver.quit()
                    raise SystemExit
            except:
                print "Not Sure What Error but Kena Exception"
                savedata("regnum", big_list_of_regnum)
                driver.quit()
                raise SystemExit
else:
    loadsettings(sys.argv[1])
    data = big_list_of_regnum
    regnumkeys = big_list_of_regnum.keys()
    total_num_of_keys = len(regnumkeys)
    print "Number of Records to scrape: " + str(total_num_of_keys)
    currentkey = 0
    # continue from previous
    if len(sys.argv) == 3:
        loadsettings("extracted_" + filename)
        data = big_list_of_regnum
        currentkey = int(sys.argv[2]) - 1
    else:
        pass
    while currentkey < total_num_of_keys:
        recordnum = currentkey + 1


        # wait for load, check if reg name same if not Back to Search Results
        loader = 0
        while loader < 10:
            # go to record
            print "going record " + str(recordnum)
            time.sleep(1)
            print "waiting for jQuery"
            wait = WebDriverWait(driver, 60)
            try:
                wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                view_more_details = '$("#regNo").val("' + \
                    regnumkeys[currentkey] + \
                    '"); $("#getSearchSummary").attr("action", "getSearchDetails.action"); ' \
                    '$("#getSearchSummary").submit();'

                driver.execute_script(view_more_details)

            except Exception as e:
                pass

            time.sleep(1)
            wait = WebDriverWait(driver, 60)
            try:
                print "Try #" + str(loader)
                wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    #.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Back to Search Results")))
                if driver.find_element_by_xpath(xpath_regnum).text == str(regnumkeys[currentkey]):
                    print "CurrentKey and Current Record SAME"
                    break
                else:
                    print "CurrentKey and Current Record DIFFERENT"
                    print "retrying record number " + str(recordnum)
                    #driver.execute_script(view_more_details)
                    driver.execute_script('backToSearchResults()')
                    #driver.execute_script('viewMoreDetails("%s")' % str(regnumkeys[currentkey]))
            except:
                print "Page not loaded..."
                print "Retry #"+str(loader)
                print "retrying record number " + str(recordnum)
                #driver.execute_script(view_more_details)
                #driver.execute_script('viewMoreDetails("%s")' % str(regnumkeys[currentkey]))
                #print "waiting for load"
                loader += 1

        # extract retails
        print "extracting record number %i / %i" % (recordnum, total_num_of_keys)
        extractdetails()
        savedata("extracted_", data)
        # go back search
        # driver.back()
        # driver.get(url)
        driver.execute_script('backToSearchResults()')
        print "wait 1s"
        time.sleep(1)
        # driver.execute_script("backToSearchResults()")
        # driver.switch_to.frame("msg_main")
        # wait for load //*[@class="red-color no-decoration underline" and starts-with(.,'Reset')]
        currentkey += 1


#     "Registration Num":{
#         "Name":"",
#         "PCSD":"", # Practicing Cert Start Date DDMMYYYY from dd/mm/yyyy format
#         "PCED":"", # Practicing Cert End Date DDMMYYYY from dd/mm/yyyy format
#         "Qualifications":[
#             [
#                 "Type",
#                 "Course"
#                 "Year"
#                 "School"
#                 "Country"
#             ]
#         ],
#         "Profession":""
#         "RegDate":"", # Date of Registration DDMMYYYY from dd/mm/yyyy format
#         "RegType":"",
#         "Primary Practice":[
#                 "Name",
#                 "Address",
#                 "Postal Code"
#             ]
#         "Secondary Practice":[
#             [
#                 "Name",
#                 "Address",
#                 "Postal Code"
#             ]
#        ]
#     }
"""
create_list_records()
print "creating list records"
num_in_list = len(list_records)
listcount = 0
while listcount < num_in_list:
    # Wait for page to load
    loader = 0
    while loader < 10:
        try:  # wait for load
            element = WebDriverWait(driver, 3) \
                .until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "View more details")))
            break
        except:
            print "waiting for load"
            loader += 1

    # create_list_records()
    # list_records[listcount].click()
    driver.execute_script(list_records[listcount])
    extractdetails()
    driver.execute_script("backToSearchResults()")
    # driver.find_element_by_partial_link_text("Back to Search Results").click()
    print "back to search results"
    time.sleep(1)
    listcount += 1

# continue from page
global page
if len(sys.argv) < 2:
    page = 1
    pass
else:
    page = int(sys.argv[1])
    driver.execute_script("gotoPageDEFAULT(" + str(page) + ")")
    print "going page " + str(page)
    # Wait for page to load
    time.sleep(3)
    loader = 0
    while loader < 10:
        try:  # wait for load
            element = WebDriverWait(driver, 3) \
                .until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "View more details")))
            break
        except:
            print "waiting for load"
            loader += 1
"""
