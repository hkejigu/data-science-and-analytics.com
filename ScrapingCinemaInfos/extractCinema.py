import time
import datetime

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
from bs4 import BeautifulSoup

# http://dryscrape.readthedocs.org/en/latest/index.html
import dryscrape

today = datetime.datetime.now();
todayString = ("%s-%s-%s" % (today.year, today.month, today.day))

city = "bayreuth"
url = "http://www.cineplex.de/"+city+"/programm/#im-kino/" + todayString

session = dryscrape.Session()
session.visit(url)

# necessary because loading all javascript content
# optimize with wait_for
time.sleep(10)

page = session.body()

# parse code and store it in BeautifulSoap format
soup = BeautifulSoup(page, "html.parser")
# print soup.prettify()

movies = soup.find_all("div", attrs={"class": "single-item single-film"})

for movie in movies:
    movieTitle = movie.find("a", attrs={"class": "filmInfoLink"}).get_text()
    try:
        movieRuntime = movie.find("span", attrs={"class": "runtime"}).get_text().strip()
    except AttributeError:
        movieRuntime = ""
    movieLength = movie.find("span", attrs={"class": "length"}).get_text().strip()
    movieGenre = movie.find("span", attrs={"class": "genre"}).get_text().strip()
    print "Movie: " + movieTitle
    print "Runtime: " + movieRuntime
    print "Length: " + movieLength
    print "Genre: " + movieGenre

    #Times
    runningTimesTable = movie.find("table", attrs={"class": "times times-single-day"})
    runningTimes = runningTimesTable.find_all("tr")

    print "Running Times:"
    print "****************************"
    for row in runningTimes:
        movie2d3d = row.find("th").get_text().strip()
        print movie2d3d
        for time in row.find_all("a", attrs={"class": "btn-runningtime"}):
            movieTime = time.get_text().strip()
            print movieTime
        print "++++++++++++++++++++++++++++"
    print "============================\n"
