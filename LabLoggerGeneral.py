import mechanize
import time

spu_username = <YOUR_USERNAME_HERE>
spu_password = <YOUR_PASSWORD_HERE>


# Browser
br = mechanize.Browser()


def main():

    # Browser options
    br.set_handle_equiv( True ) 
    br.set_handle_gzip( True ) 
    br.set_handle_redirect( True ) 
    br.set_handle_referer( True ) 
    br.set_handle_robots( False ) 
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # login/auth
    response = br.open("https://banweb.spu.edu/pls/prod/twbkwbis.P_WWWLogin")    

    handleFirstWindow(br)
    handleLoginToSPU()
    handleTimesheetSelection()
    handleUpdateTimesheet()

    print("Good shit\n")




# Get today's url, but might need to figure out the LastDate= part
# and maybe it will change throughout the weeks
def getTodaysURL():
    month = time.strftime("%b").upper()
    day = time.strftime("%d")
    year = time.strftime("%Y")
    # MAKE SURE YOU CHANGE THIS URL TO YOUR OWN PERSONAL. COPY DOWN THE URL WHERE YOU ENTER YOUR HOURS.
    # MAKE SURE YOU PUT IN THE %s FOR MONTH, DATE, YEAR LIKE SO
    # return "YOUR_URL...&DateSelected=%s-%s-%s&LineNumber=5" % (day, month, year)


# Handle First form window with single sign-on prompt
def handleFirstWindow():
    br.select_form(nr=0)
    br.set_all_readonly( False )
    br.submit()

# Handle logging into actual SPU system
def handleLoginToSPU():
    br.select_form(nr=0)
    br["username"] = spu_username
    br["password"] = spu_password
    br.submit()
    
# Choose timesheet so that we can go ahead and update/get access to html form that allows update.
def handleTimesheetSelection():
    req = mechanize.Request("https://banweb.spu.edu/pls/prod/bwpktais.P_SelectTimeSheetRoll")
    br.open(req)
    br.select_form(nr=1)
    br.set_all_readonly( False )
    br.submit(type="submit")

# Update your timesheet with times of when one worked.
def handleUpdateTimesheet():
    # Find Today's time sheet
    todaysURL = getTodaysURL()
    timesheet = mechanize.Request(todaysURL)
    br.open(timesheet)
    br.select_form(nr=1)
    br.set_all_readonly ( False )
    
    # Update timesheet
    timeIN = br.find_control(name="TimeIn", nr=0)
    timeIN.value = "6:00"
    timeOUT = br.find_control(name="TS_TimeOut", nr=0)
    timeOUT.value = "9:30"

    timeIN_AMPM = br.find_control(name="TimeInAm", nr=0)
    timeIN_AMPM.value = ["PM"]
    timeOUT_AMPM = br.find_control(name="TimeOutAm", nr=0)
    timeOUT_AMPM.value = ["PM"]

    br.submit(name="ButtonSelected", label="Save")

if __name__ == "__main__":
    main()
