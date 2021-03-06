# Standard imports
import os
import time
import re
import sqlite3
import xmlrpc.client
from datetime import datetime, date

# Custom imports
import kat
import queuer
import torrentdl
import tvshows
import settings


seconds = 1
minute = 60 * seconds
hour = 60 * minute
halfhour = 0.5 * hour

def normalize_name(name):
    name = re.sub("[ .)(}{_-]+", "_", name)
    name = name.lower()

    return name

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
             "  tvshows.torrent_kws, episodes.episodeid, episodes.airdate "
             "FROM episodes JOIN tvshows USING (showid) "
             "WHERE episodes.status = 'QUEUED'")
    cur.execute(query)
    rows = cur.fetchall()
    today = date.today()
    for row in rows:
        # If this episode releases in the future, don't bother trying to
        # download it now and just skip it.
        # NOTE: This relies on the info provided by tvrage.com to be correct.
        airdate = datetime.strptime(row[-1], '%Y-%m-%d')
        if airdate.date() > today:
            continue
        # Construct the torrent search string.
        search_string = "%s S%02dE%02d %s" % (row[0], row[1], row[2], row[4])
        print("Searching KAT for \"%s\" ..." % search_string)
        torrents = kat.search(search_string, category=kat.Categories.TV,
                              sort=kat.Sorting.SEED, order=kat.Sorting.Order.DESC)
        # If no torrents found for this download, then maybe no torrents are
        # released yet. So just skip it for now.
        if len(torrents) == 0:
            print("No torrents found. Skipping ...")
            print()
            continue
        # We only need one "best" torrent.
        torrent = torrents[0]
        print("Adding torrent for download:", torrent.title)
        print()

        download_dir = os.path.join(settings.dl_path, normalize_name(row[0]))
        opts = {'dir': download_dir}
        meta_gid = s.aria2.addUri([torrent.magnet], opts)
        # Get the gid of the actual download that was started by this metalink
        # download.
        while True:
            try:
                meta_status = s.aria2.tellStatus(meta_gid)
                gid = meta_status['followedBy'][0]
                break
            except:
                time.sleep(1)
                pass
        status = s.aria2.tellStatus(gid)
        destination = os.path.join(status['dir'],
                                   status['bittorrent']['info']['name'])
        episodeid = row[5]
        query = ("UPDATE episodes "
                 "SET status = 'DOWNLOADING', destination = ? "
                 "WHERE episodeid = ?")
        cur.execute(query, (destination, episodeid))
        conn.commit()

    # Now if there are any episodes that have completed downloading, then update
    # their status.
    query = ("SELECT episodes.episodeid, episodes.destination "
             "FROM episodes "
             "WHERE episodes.status = 'DOWNLOADING'")
    cur.execute(query)
    rows = cur.fetchall()
    # Check with aria2 to see if any of the DOWNLOADING episodes finished. For
    # every such episode, set the status to be COMPLETED.
    # If the destnation.aria2 file exists, then the file is still not finished.
    for row in rows:
        if not os.path.exists(row[1] + '.aria2'):
            query = ("UPDATE episodes "
                     "SET status='COMPLETED' "
                     "WHERE episodeid=?")
            values = (row[0],)
            cur.execute(query, values)
        conn.commit()

    # Now check to see if any of the tv shows have new episodes announced.
    query = ("SELECT tvshows.showid, tvshows.name "
             "FROM tvshows")
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        showid = row[0]
        showname = row[1]
        # Try to search episodes but if there's a failure, just skip.
        try:
            print("Searching TVRage for new episodes for \"%s\" ..." % showname)
            episodes = tvshows.search_episodes(showid)
        except:
            print("Unable to get new eipsodes. Skipping ...")
            print()
            continue
        # Get the largest recorded episode number.
        query = ("SELECT MAX(episode_number) "
                 "FROM episodes "
                 "WHERE showid=?")
        values = (showid,)
        cur.execute(query, values)
        largest_episode_number = cur.fetchone()[0]
        # Now add all the episodes with episode number larger than the largest
        # one so far.
        enqueued_episodes = 0
        for episode in episodes:
            if episode['episode_number'] > largest_episode_number:
                try:
                    # If it's a valid date, then enqueue the episode.
                    time.strptime(episode['airdate'], '%Y-%m-%d')
                    queuer.enqueue_episode(episode, cur)
                    enqueued_episodes += 1
                except ValueError:
                    pass
        print("Enqueued %d new eipsodes." % enqueued_episodes)
        print()
        conn.commit()

if __name__ == '__main__':
    while True:
        poller(settings.db_path)
        time.sleep(halfhour)
