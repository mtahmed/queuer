# Standard imports
import time
import sqlite3
import xmlrpc.client

# Custom imports
import libtpb
import enqueue
import torrentdl
import tvshows
import settings


seconds = 1
minute = 60 * seconds
hour = 60 * minute
halfhour = 0.5 * hour

def poller(db):
    '''
    The poller wakes up every 30 minutes and does the following checks:
    - Are there any undownloaded episodes released in the past? If yes, it tries
      to find a torrent for that episode and downloads the torrent if it finds
      it feasible.
    - Are there any queued tv shows that have new announced episodes? If yes, it
      enqueues the new episodes.
    '''
    # Database connection
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # aria2 xmlrpc connection
    s = xmlrpc.client.ServerProxy("http://localhost:6800/rpc")

    # First check to see if there are QUEUED episodes that are to be downloaded.
    query = ("SELECT tvshows.name, episodes.season_number, "
             "  episodes.season_episode_number,  episodes.episode_number, "
             "  tvshows.torrent_kws "
             "FROM episodes JOIN tvshows USING (showid) "
             "WHERE episodes.status = 'QUEUED'")
    cur.execute(query)
    rows = cur.fetchall()
    print(len(rows))
    for row in rows:
        # Construct the torrent search string.
        search_string = "%s S%02dE%02d %s" % (row[0], row[1], row[2], row[4])
        print(search_string)
        torrents = libtpb.search_torrents(search_string)
        # If no torrents found for this download, then maybe no torrents are
        # released yet. So just skip it for now.
        if len(torrents) == 0:
            continue
        # We only need one "best" torrent.
        torrent = torrents[0]
        gid = s.aria2.addUri([torrent['magnet']])

    # Now if there are any episodes that have completed downloading, then update
    # their status.
    query = ("SELECT episodes.gid "
             "FROM episodes "
             "WHERE episodes.status = 'DOWNLOADING'")
    cur.execute(query)
    rows = cur.fetchall()
    # Check with aria2 to see if any of the DOWNLOADING episodes finished. For
    # every such episode, set the status to be COMPLETED.
    for row in rows:
        gid = row[0]
        status = s.aria2.tellStatus(gid, ['status'])['status']
        if status == 'complete':
            s.aria2.pause(gid)
        query = ("UPDATE episodes "
                 "SET status='COMPLETED' "
                 "WHERE gid=?")
        values = (gid,)
        cur.execute(query, values)

    # Now check to see if any of the tv shows have new episodes announced.
    query = ("SELECT tvshows.showid "
             "FROM tvshows")
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        showid = row[0]
        episodes = tvshows.search_episodes(showid)
        # Get the largest recorded episode number.
        query = ("SELECT MAX(episode_number) "
                 "FROM episodes "
                 "WHERE showid=?")
        values = (showid,)
        cur.execute(query, values)
        largest_episode_number = cur.fetchone()[0]
        # Now add all the
        for episode in episodes:
            if episode[episode_number] > largest_episode_number:
                if episode['airdate'] != '0000-00-00':
                    enqueue.enqueue_episode(episode, cur)

if __name__ == '__main__':
    while True:
        poller(settings.db_path)
        time.sleep(halfhour)
