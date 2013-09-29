# Standard imports
import time
import sqlite3

# Custom imports
import libtpb
import enqueue
import torrentdl
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
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # First check to see if there are QUEUED episodes that are to be downloaded.
    cur.execute('''SELECT * FROM episodes JOIN tvshows USING (showid)
WHERE episodes.status = 'QUEUED'''')
    rows = cur.fetchall()
    for row in rows:
        # Construct the torrent search string.
        search_string = 

if __name__ == '__main__':
    poller(settings.db_path)
