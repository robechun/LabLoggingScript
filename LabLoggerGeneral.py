import mechanize
import time
from bs4 import BeautifulSoup

# ------------------------ !!CHANGE HERE!! ------------------------- #
spu_username = "<YOUR_USERNAME_HERE>"
spu_password = "<YOUR_PASSWORD_HERE>"
# ------------------------------------------------------------------ #


# Browser
br = mechanize.Browser()

# -------------------------------------- !!CHANGE HERE!! ------------------------------------------ #
# # Days you are going to be working -- put into form "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
workingDays = ("Mon", "Tue", "Wed")
# ------------------------------------------------------------------------------------------------- #

def main():

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; '
                      'rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 '
                      'Firefox/3.0.1')]

    br.open("https://banweb.spu.edu/pls/prod/twbkwbis.P_WWWLogin")

    if checkWorkingDay() is False:
        print "Today is not a day in your shift!"
        return
    handleFirstWindow()
    handleLoginToSPU()
    handleTimesheetSelection()
    handleUpdateTimesheet()

    print("Good shift m8\n")


# Get today's url, but might need to figure out the LastDate= part
# and maybe it will change throughout the weeks
def getTodaysURL():
    # Grab today's date to figure out which section to insert
    month = time.strftime("%b").upper()
    day = time.strftime("%d")
    year = time.strftime("%Y")

    # Grab the url to redirect to
    response = br.response()
    soup = BeautifulSoup(response.read(), "html.parser")
    table = soup.find_all("td", class_="dbdefault")
    url = table[5].find('a').get('href')
    url = "https://banweb.spu.edu" + url[:url.index("DateSelected=")] + \
          "DateSelected=%s-%s-%s" % (day, month, year) + "&LineNumber=5"

    return url


# Handle First form window with single sign-on prompt
def handleFirstWindow():
    br.select_form(nr=0)
    br.set_all_readonly(False)
    br.submit()


# Handle logging into actual SPU system
def handleLoginToSPU():
    br.select_form(nr=0)
    br["username"] = spu_username
    br["password"] = spu_password
    br.submit()
    

# Choose timesheet so that we can go ahead and update/get access to html form
# that allows update.
def handleTimesheetSelection():
    req = mechanize.Request("https://banweb.spu.edu/pls/prod/bwpktais"
                            ".P_SelectTimeSheetRoll")
    br.open(req)
    br.select_form(nr=1)
    br.set_all_readonly(False)
    br.submit(type="submit")


# Update your timesheet with times of when one worked.
def handleUpdateTimesheet():

    # Grab previous hours before logging
    hours = getHours()
    print "PREV HOURS: ", hours

    # Find Today's time sheet
    todaysURL = getTodaysURL()
    timesheet = mechanize.Request(todaysURL)
    br.open(timesheet)
    br.select_form(nr=1)
    br.set_all_readonly(False)
    
    # Update timesheet
    timeIN = br.find_control(name="TimeIn", nr=0)
    timeOUT = br.find_control(name="TS_TimeOut", nr=0)
    timeIN_AMPM = br.find_control(name="TimeInAm", nr=0)
    timeOUT_AMPM = br.find_control(name="TimeOutAm", nr=0)
    
    # Change this based on your own shift!
    day = time.strftime("%a")

    # ------------------------ !!CHANGE HERE!! ------------------------- #
    # Thu, Fri, Sat, Sun are available
    # Simply change the values depending on when your regular shifts are
    if day == "Mon":
        timeIN.value = "6:00"
        timeOUT.value = "9:30"
        timeIN_AMPM.value = ["PM"]
        timeOUT_AMPM.value = ["PM"]
    elif day == "Tue":
        timeIN.value = "6:00"
        timeOUT.value = "9:30"
        timeIN_AMPM.value = ["PM"]
        timeOUT_AMPM.value = ["PM"]
    elif day == "Wed":
        timeIN.value = "6:00"
        timeOUT.value = "9:30"
        timeIN_AMPM.value = ["PM"]
        timeOUT_AMPM.value = ["PM"]
    else:
        print "ERROR: Check your working days or script for typos"
        return
    # ------------------------------------------------------------------ #

    br.submit()

    hours = getHours()
    print "AFTER TODAY: ", hours


# Tbh not the best way to do this but it should work for this application
def getHours():
    # Report to user current total hours
    response = br.response()
    soup = BeautifulSoup(response.read(), "html.parser")
    table = soup.find_all("td", class_="dbdefault")
    hours = table[3].find('p').getText()
    return hours


def checkWorkingDay():
    day = time.strftime("%d")
    if day in workingDays:
        return True
    
    return False


if __name__ == "__main__":
    print "---------------------------------------------"
    print "|          Logging your hours               |"
    print "---------------------------------------------"
    main()
