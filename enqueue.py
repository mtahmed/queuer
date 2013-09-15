# Standard imports
import sqlite3

# Custom imports
import libtpb
import tvshows
import settings

def init_db(conn, cur):
    '''
    Create the basic table structure for the database with the connection conn
    and cursor cursor.
    '''
    # Create the shows table.
    cur.execute('''CREATE TABLE tvshows (showid INTEGER, name TEXT, link TEXT,
started TEXT, seasons INTEGER, airtime TEXT, airday TEXT, torrent_kws TEXT)''')
    # Create the episode table.
    cur.execute('''CREATE TABLE episodes (showid INTEGER, season_number INTEGER,
episode_number INTEGER, title TEXT, airdate TEXT, status VARCHAR(10))''')

    return

def enqueue_episode(episode, torrent_kws, cur):
    '''
    Enqueue (add to database) one episode.
    '''
    cur.execute('''INSERT INTO episodes VALUES (?, ?, ?, ?, ?, ?, 'QUEUED')''',
                   (episode['showid'], episode['season_number'],
                    episode['episode_number'], episode['title'],
                    episode['airdate'], torrent_kws))

    return

def enqueue(db):
    tvshow_query = input("Enter tv show name: ")
    torrent_kws = input("Enter other keywords to search for torrents"
                        " (e.g. 720p eztv): ")

    shows = tvshows.search_tvshows(tvshow_query)

    print("Found %d tv show(s)!\n" % len(shows))

    for count, show in enumerate(shows):
        tvshows.print_tvshow(show, count)

    while True:
        show_index = int(input("Enter tv show number: "))
        if show_index >= 0 and show_index <= count:
            break

    show = shows[show_index]

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
            airdate = datetime.strptime(episode['airdate'], '%Y-%m-%d')
            if airdate.date() > today:
                enqueue_episodes.append(episode)
    # List all the episodes and the user selects which episodes to download.
    elif which == 'list' or which == 'l':
        for count, episode in enumerate(episodes):
            tvshows.print_episode(episode, count)
        # The list can be either an episode index or a  list of episode indices
        # or it can be a range like 10-20 (inclusive) or a list of ranges or a
        # list of ranges and indices.
        print()
        ep_list = (input("Enter episodes (or ranges) to download: ")).split(' ')
        for ep in ep_list:
            ep_range = [int(ep_index) for ep_index in ep.split('-')]
            if len(ep_range) == 2:
                for ep_index in range(ep_range[0], ep_range[1] + 1):
                    enqueue_episodes.append(episodes[ep_index])
            elif len(ep_range) == 1:
                enqueue_episodes.append(episodes[int(ep)])
    else:
        raise Exception('You idiot!')

    # Now that we know which episodes to enqeue, we need to open a connection to
    # the database and add all the episodes.
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute('SELECT * FROM sqlite_master WHERE type=\'table\'')
    if len(cur.fetchall()) == 0:
        init_db(conn, cur)

    # Lock the database for this transaction.
    while True:
        try:
            cur.execute('BEGIN IMMEDIATE TRANSACTION')
        except sqlite3.OperationalError as e:
            if e == 'database is locked':
                print('Database locked for transaction. Retrying ...')
    # Now add the episodes one at a time.
    for episode in enqueue_episodes:
        enqueue_episode(episode, torrent_kws, cur)
    # Now unlock the database by committing the transaction.
    cur.execute('COMMIT TRANSACTION')

if __name__ == '__main__':
    enqueue(settings.db_path)
