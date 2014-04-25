# Standard imports
import argparse
import sqlite3
from datetime import datetime, date

# Custom imports
import tvshows
import settings

def init_db(conn, cur):
    '''
    Create the basic table structure for the database with the connection conn
    and cursor cursor.
    '''
    # Create the shows table.
    # Schema:
    # showid | name | link | started | seasons | airtime | airday | torrentkws
    query = ("CREATE TABLE tvshows "
             "(showid INTEGER, name TEXT, link TEXT, started TEXT, "
             "seasons INTEGER, airtime TEXT, airday TEXT, torrent_kws TEXT)")
    cur.execute(query)
    # Create the episode table.
    # Schema:
    # showid | seasons_number | seasons_episode_number | episode_number | title
    # | airdate | status | destination
    query = ("CREATE TABLE episodes "
             "(episodeid INTEGER, showid INTEGER, season_number INTEGER, "
             "season_episode_number INTEGER, episode_number INTEGER, "
             "title TEXT, airdate TEXT, status VARCHAR(16), destination TEXT)")
    cur.execute(query)

    return

def enqueue_episode(episode, cur):
    '''
    Enqueue (add to database) one episode.
    '''
    cur.execute("INSERT INTO episodes VALUES (?, ?, ?, ?, ?, ?, ?, 'QUEUED', '')",
                (episode['episodeid'], episode['showid'], episode['season_number'],
                 episode['season_episode_number'], episode['episode_number'],
                 episode['title'], episode['airdate']))

    return

def add_tvshow(show, torrent_kws, cur):
    '''
    Add a tvshow to database.
    '''
    cur.execute("INSERT INTO tvshows VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (show['showid'], show['name'], show['link'], show['started'],
                 show['seasons'], show['airtime'], show['airday'], torrent_kws))

    return

def dequeue(conn, cur):
    '''Dequeue episode(s).
    '''
    query = ("SELECT * FROM tvshows")
    cur.execute(query)
    tvshows = cur.fetchall()
    num_tvshows = len(tvshows)

    for count, tvshow in enumerate(tvshows, start=1):
        print("%2d: %s (%s)" % (count, tvshow[1], tvshow[3]))
        print()

    which = input("Which tvshows to dequeue?\n[space-separated list]: ")
    which = [int(num) for num in which.split(' ')]

    num_removed = 0
    for num in which:
        if num > 0 and num <= num_tvshows:
            showid = tvshows[num-1][0]

            query = ("DELETE FROM tvshows WHERE "
                     "showid = ?")
            values = (showid,)
            cur.execute(query, values)

            query = ("DELETE FROM episodes WHERE "
                     "showid = ?")
            values = (showid,)
            cur.execute(query, values)

            conn.commit()
            num_removed += 1

    print()
    print("Removed %d tvshow(s)!" % num_removed)

    return

def enqueue(conn, cur):
    '''
    The main user-facing function that prompts user for inputs like the tv show
    name, the keywords, the episodes that they need to download etc. and based
    on the selections by the user, downloads the appropriate episodes.
    '''
    tvshow_query = input("Enter tv show name: ")
    torrent_kws = input("Enter other keywords to search for torrents"
                        " (e.g. 720p eztv): ")

    shows = tvshows.search_tvshows(tvshow_query)

    print("Found %d tv show(s)!\n" % len(shows))

    # Print all the tvshows found.
    for count, show in enumerate(shows, start=1):
        tvshows.print_tvshow(show, count)

    # Get user input for which tvshow they are looking for.
    while True:
        show_index = int(input("Enter tv show number: "))
        if show_index >= 0 and show_index <= count:
            break

    show = shows[show_index-1]

    episodes = tvshows.search_episodes(show['showid'])

    print("Found %d episode(s)!\n" % len(episodes))

    which = input("Which episodes to enqueue?\n[a(ll), f(uture), l(ist)]: ")
    # This is basically asking to enqueue all the episodes found.
    if which == 'all' or which == 'a' or which == '':
        enqueue_episodes = episodes
    # Only enqueue the future episodes.
    elif which == 'future' or which == 'f':
        today = date.today()
        enqueue_episodes = []
        for episode in episodes:
            try:
                airdate = datetime.strptime(episode['airdate'], '%Y-%m-%d')
            except ValueError:
                continue
            if airdate.date() >= today:
                enqueue_episodes.append(episode)
    # List all the episodes and the user selects which episodes to download.
    elif which == 'list' or which == 'l':
        for episode in episodes:
            tvshows.print_episode(episode)
        # The list can be either an episode index or a  list of episode indices
        # or it can be a range like 10-20 (inclusive) or a list of ranges or a
        # list of ranges and indices.
        print()
        ep_list = (input("Enter episodes (or ranges) to queue: ")).split(' ')
        for ep in ep_list:
            ep_range = [int(ep_index) for ep_index in ep.split('-')]
            if len(ep_range) == 2:
                for ep_index in range(ep_range[0], ep_range[1] + 1):
                    enqueue_episodes.append(episodes[ep_index-1])
            elif len(ep_range) == 1:
                enqueue_episodes.append(episodes[int(ep)-1])
    else:
        raise Exception('You idiot!')

    # If the tvshow is not in database, add the tvshow first.
    cur.execute('SELECT * FROM tvshows WHERE showid=?', (show['showid'],))
    if len(cur.fetchall()) == 0:
        add_tvshow(show, torrent_kws, cur)
        conn.commit()


    # Now add the episodes one at a time.
    for episode in enqueue_episodes:
        # If the episode airdate is 0000-00-00, then the episode information
        # is not yet available.
        if episode['airdate'] != '0000-00-00':
            enqueue_episode(episode, cur)

    conn.commit()

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="manage the queue")
    parser.add_argument("-e", "--enqueue", action="store_true",
                        help="enqueue episode(s)")
    parser.add_argument("-d", "--dequeue", action="store_true",
                        help="dequeue episode(s)")
    args = parser.parse_args()

    db = settings.db_path
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # If the database is not initialized yet, initialize it.
    cur.execute('SELECT * FROM sqlite_master WHERE type=\'table\'')
    if len(cur.fetchall()) == 0:
        init_db(conn, cur)
        conn.commit()


    if args.enqueue:
        enqueue(conn, cur)
    elif args.dequeue:
        dequeue(conn, cur)
    else:
        parser.print_help()
