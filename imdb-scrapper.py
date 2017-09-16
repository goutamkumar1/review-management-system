# Simple IMDB scraping script
# David Dohan
import urllib2
import bs4
import sys
import time
import json


def scrape_movies(url):
    html = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(html)

    titles = soup.findAll("td", "title")

    movies = []

    for title in titles:
        try:
            # First hyperlink is the title
            name = title.find("a").text

            # Release date
            # <span class="year_type">(2003)</span>

            year = title.find("span", "year_type").text

            # User rating
            # <div class="user_rating">
            # <div class="rating rating-list" id="tt0266543|imdb|8.2|8.2|advsearch">
            # ...
            # </div>
            rating = title.find("div", "rating").attrs['id'].split('|')[-2]

            # Outline/synopysis
            # <span class="outline">After his ...</span>
            outline_span = title.find("span", "outline")
            if outline_span:
                outline = outline_span.text

            # Get actors and directors
            # <span class="credit">
            # Dir: <a href="/name/nm0004056/">Andrew Stanton</a>, <a href="/name/nm0881279/">Lee Unkrich</a>
            # With: <a href="/name/nm0000983/">Albert Brooks</a>,
            #    <a href="/name/nm0001122/">Ellen DeGeneres</a>, <a href="/name/nm1071252/">Alexander Gould</a>
            # </span>
            directors = []
            actors = []
            state = None  # actors or directors
            for s in title.find("span", "credit").children:
                if "Dir" in s:
                    state = 'dir'
                elif "With" in s:
                    state = 'act'
                elif type(s) is bs4.element.Tag:
                    if state is 'dir':
                        directors.append(s.text)
                    elif state is 'act':
                        actors.append(s.text)
                    else:
                        print("Wat")
                        pass

            # Scrape set of genres
            # <span class="genre"><a href="/genre/comedy">Comedy</a> |
            #       <a href="/genre/drama">Drama</a> | <a href="/genre/sci_fi">Sci-Fi</a></span>
            genres = [genre.text for genre in title.find("span", "genre").findAll("a")]

            # "100 mins. -> 100"
            # <span class="runtime">103 mins.</span>
            runtime_span = title.find("span", "runtime")
            runtime = None
            if runtime_span:
                runtime = runtime_span.text.split()[0]


            # Rating is the first class of the inner span
            # <span class="certificate"><span class="us_pg titlePageSprite"></span></span>
            certificates = title.find("span", "certificate")
            mpaa = None
            if certificates:
                cert_span = certificates.find("span")
                if cert_span is not None:
                    mpaa = cert_span.attrs['class'][0]

            movies.append({"name": name,
                           "year": year,
                           "rating": rating,
                           "outline": outline,
                           "directors": directors,
                           "actors": actors,
                           "genres": genres,
                           "runtime": runtime,
                           "mpaa": mpaa})
        except:
            print("Error while processing {}".format(url))
    return movies


def scrape_many(start=1,
                step=50,
                pages=10,
                second_delay=1,
                url_format="http://m.imdb.com/search/title?at=0&sort=num_votes,desc&start={start}"):
    """
    Start at _start_, increase in steps of size _step_, and scrape _pages_ pages total

    Default IMDB url loads 50 movies per page
    """
    movies = []
    for i in range(pages):
        print("Scraping results starting at {}".format(start))
        movies.extend(scrape_movies(url_format.format(start=start)))
        start += step
        time.sleep(second_delay)
    return movies


def save_movies(movies, path):
    with open(path, 'w') as f:
        json.dump(movies, f, sort_keys=True, indent=4,
                  separators=(',', ': '))

def load_movies(path):
    with open(path, 'r') as f:
        movies = json.load(f)
	return movies