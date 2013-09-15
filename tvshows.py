# Standard imports
from datetime import datetime, date
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup


class TVShow(object):
    def __init__(self, showid, name, link, started, seasons, airtime, airday):
        self.showid  = showid
        self.name    = name
        self.link    = link
        self.started = started
        self.seasons = seasons
        self.airtime = airtime
        self.airday  = airday


class Episode(object):
    def __init__(self, episodeid, showid, season_number, episode_number, title,
                 airdate):
        self.episodeid      = episodeid
        self.showid         = showid
        self.season_number  = season_number
        self.episode_number = episode_number
        self.title          = title
        self.airdate        = airdate

    def get_show(cur):
        cur.execute('''SELECT * FROM tvshows WHERE showid=?''', (self.showid,))
        row = cur.fetchone()
        return TVShow(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                      row[7])

def search_tvshows(query):
    search_url = 'http://services.tvrage.com/feeds/full_search.php?show='
    quoted_query = quote(query)

    doc_file = urlopen(search_url + quoted_query)

    soup = BeautifulSoup(doc_file.read())
    search_results = soup.find_all('show')

    tvshows = []
    for search_result in search_results:
        showid = int(search_result.find('showid').string)
        name = search_result.find('name').string
        link = search_result.find('link').string
        started = search_result.find('started').string
        seasons = int(search_result.find('seasons').string)
        airtime = search_result.find('airtime').string
        airday = search_result.find('airday').string

        tvshow = {'showid'    : showid,
                  'name'      : name,
                  'link'      : link,
                  'started'   : started,
                  'seasons'   : seasons,
                  'airtime'   : airtime,
                  'airday'    : airday}

        tvshows.append(tvshow)

    return tvshows

def print_tvshow(tvshow, count):
    print("%2d: %s (%s)" % (count, tvshow['name'], tvshow['started']))
    print("    Seasons: %s" % tvshow['seasons'])
    print("    Airs %s every %s" % (tvshow['airtime'], tvshow['airday']))
    print("    %s" % tvshow['link'])
    print()

def search_episodes(showid):
    search_url = 'http://services.tvrage.com/feeds/episode_list.php?sid='

    doc_file = urlopen(search_url + str(showid))

    soup = BeautifulSoup(doc_file.read())

    episodes = []
    for season_soup in soup.select('show > episodelist > season'):
        season_number = int(season_soup['no'])
        for ep_soup in season_soup.find_all('episode'):
            episode_number = int(ep_soup.find('seasonnum').string)
            ep_id = int('%d%02d%02d' % (showid, season_number, episode_number))
            ep = {'episodeid'      : ep_id,
                  'showid'         : showid,
                  'season_number'  : season_number,
                  'episode_number' : episode_number,
                  'title'          : ep_soup.find('title').string,
                  'airdate'        : ep_soup.find('airdate').string}
            episodes.append(ep)

    return episodes

def print_episode(episode, count):
    print("%2d: s%02de%02d - %-40s (%s)" % (count,
                                            int(episode['season_number']),
                                            int(episode['episode_number']),
                                            episode['title'],
                                            episode['airdate']))
