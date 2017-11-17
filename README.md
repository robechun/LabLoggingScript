# Lab Logging Script

## Script to log hours within the SPU Banner System.

<i><b>Written in Python and using Mechanize.</i></b>


To use, either clone my repo or copy paste the script into your own python script.

Then, change the <SPU_USERNAME> field and <SPU_PASSWORD> field with your information.
Look at the update time sheet function and follow my instructions (comments) to populate the correct information based on your own shift times.


You need two libraries for this script to work: <b>Mechanize and BeautifulSoup</b>

[Mechanize](http://wwwsearch.sourceforge.net/mechanize/download.html)


[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/#Download)

<i>alternatively for beautiful soup</i>, if you have pip installed, just do ```pip install beautifulsoup4```

----

Running the script will automatically log your hours for that day.

## TODO

- [x] Be able to support other users 
- [x] Handle customizable times for logging
- [ ] Cookies(?)
